import logging
from dataclasses import dataclass

import config
import httpx
from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

emoji_todo = ":white_medium_square:"
emoji_done = ":white_check_mark:"

EXECUTE = "EXECUTE"
CANCEL_EXECUTE = "CANCEL_EXECUTE"
ON_TASK = "ON_TASK"
OFF_TASK = "OFF_TASK"
TO_TASK_LIST = "TO_TASK_LIST"


@dataclass
class Task:
    task_uri: str
    template_uri: str
    name: str
    description: str
    is_active: bool
    task_done: bool


@dataclass
class TaskParam:
    uri: str
    is_active: bool | None = None
    task_done: bool | None = None


@dataclass
class Key:
    name: str
    param: TaskParam | None = None


def get_text_tasks(tasks_list: list[dict]) -> str:
    text: str = "Задачи на сегодня:\n\n"
    for index, task in enumerate(tasks_list, start=1):
        text += str(index)
        # time = task.get('time', '')
        if task["task_done"]:
            text += f' {emojize(emoji_done, language="alias")} ~{task["name"]}~\n'
        else:
            text += f' {emojize(emoji_todo, language="alias")} {task["name"]}\n'
    text += "\nВыберите номер задачи для просмотра"
    return text


def get_text_task(task: dict) -> str:
    text: str = f"*{task['name']}*\n\n"
    if task["task_done"]:
        text += f' {emojize(emoji_done, language="alias")} Завершено\n'
    else:
        text += f' {emojize(emoji_todo, language="alias")} Выполнить\n'
    text += f"Время \- {task.get('time', 'Не задано')}\n"
    text += f"{task.get('description', ' ')}"
    return text


async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Called /start")
    name = update.message.from_user.name
    # context.user_data['emoji'] = get_smile(context.user_data)
    # my_keyboard = main_keyboard()
    await update.message.reply_text(f"Здравствуй, {name}!")


async def show_tasks_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Called /tasks")
    if update.message:
        user_name = update.message.from_user.name
    elif update.callback_query:
        user_name = update.callback_query.from_user.name
    request = httpx.get(config.WEB + config.WEB_PARAM.format(user_name)).json()
    error = request.get("error")
    if not error:
        # task_list: list[Task] = [Task(task) for task in request["tasks"]]
        text = get_text_tasks(request["tasks"])
        keyboard = task_list_inline_keyboard(request["tasks"])
    else:
        text = error
        keyboard = None

    if update.message:
        await update.message.reply_markdown_v2(text, reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard)


async def get_context(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    callback = update.callback_query.data
    logging.info(f"Received callback {callback}")
    if callback.get("key") == EXECUTE or callback.get("key") == CANCEL_EXECUTE:
        await update_task(callback.get("uri"), callback.get("key"))
    elif callback == ON_TASK:
        logging.info(f"Called {callback}")
        pass
    elif callback == OFF_TASK:
        logging.info(f"Called {callback}")
        pass
    elif callback == TO_TASK_LIST:
        await show_tasks_list(update, context)
    else:
        await show_task(update, callback)


async def show_task(update: Update, callback: str) -> None:
    logging.info("Called show_task")
    user_name = update.callback_query.from_user.name
    request = httpx.get(callback + config.WEB_PARAM.format(user_name)).json()
    error = request.get("error")
    if not error:
        text = get_text_task(request["task"])
        keyboard = task_inline_keyboard(request["task"]["uri"], request["task"]["task_done"])
    else:
        text = error
        keyboard = None
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard)


async def update_task(uri, callback):
    logging.info("called update_task")
    # user_name = update.callback_query.from_user.name
    user_name = "@DenRyzh"
    request = httpx.get(uri + config.WEB_PARAM.format(user_name)).json()


def task_list_inline_keyboard(task_list) -> InlineKeyboardMarkup:
    inlinekeyboard = [[InlineKeyboardButton(str(i), callback_data=task["uri"]) for i, task in enumerate(task_list, 1)]]
    return InlineKeyboardMarkup(inlinekeyboard)


def task_inline_keyboard(uri: str, done: bool) -> InlineKeyboardMarkup:
    if done:
        key = CANCEL_EXECUTE
        key_txt = "Отменить выполнение"
    else:
        key = EXECUTE
        key_txt = "Выполнить"

    inlinekeyboard = [
        [
            InlineKeyboardButton(key_txt, callback_data={"key": key, "uri": uri}),
            InlineKeyboardButton("К списку", callback_data=TO_TASK_LIST),
        ]
    ]
    return InlineKeyboardMarkup(inlinekeyboard)
