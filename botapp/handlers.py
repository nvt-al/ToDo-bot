import logging

import config
import httpx
from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

emoji_todo = ":white_medium_square:"
emoji_done = ":white_check_mark:"


async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Called /start")
    # context.user_data['emoji'] = get_smile(context.user_data)
    # my_keyboard = main_keyboard()
    await update.message.reply_text("Здравствуй, пользователь!")


async def show_tasks_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text: str = "Задачи на сегодня:\n\n"
    task_list_json = httpx.get(config.WEB)
    task_list = task_list_json.json()["tasks"]
    for index, task in enumerate(task_list, start=1):
        text += str(index)
        # time = task.get('time', '')
        if task["task_done"]:
            text += f' {emojize(emoji_done, language="alias")} ~{task["name"]}~\n'
        else:
            text += f' {emojize(emoji_todo, language="alias")} {task["name"]}\n'
    text += "\nВыберите номер задачи для просмотра"
    if update.message:
        await update.message.reply_markdown_v2(text, reply_markup=task_list_inline_keyboard(task_list))


async def show_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.callback_query:
        await update.callback_query.answer()
        if update.callback_query.data:
            task_id: str = update.callback_query.data
        task_list_json = httpx.get(task_id)
        task = task_list_json.json()["task"]
        # for task in task_list:
        # if task['uri'] == task_id:
        text: str = f"*{task['name']}*\n\n"
        if task["task_done"]:
            text += f' {emojize(emoji_done, language="alias")} Завершено\n'
        else:
            text += f' {emojize(emoji_todo, language="alias")} Выполнить\n'
        text += f"Время \- {task.get('time', 'Не задано')}\n"
        text += f"{task.get('description', ' ')}"
        await update.callback_query.edit_message_text(
            text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=task_inline_keyboard()
        )


def task_list_inline_keyboard(task_list) -> InlineKeyboardMarkup:
    inlinekeyboard = [[InlineKeyboardButton(str(i), callback_data=task["uri"]) for i, task in enumerate(task_list, 1)]]
    return InlineKeyboardMarkup(inlinekeyboard)


def task_inline_keyboard() -> InlineKeyboardMarkup:
    inlinekeyboard = [
        [
            InlineKeyboardButton("Отметить", callback_data="Отметить"),
            InlineKeyboardButton("К списку", callback_data="К списку"),
        ]
    ]
    return InlineKeyboardMarkup(inlinekeyboard)
