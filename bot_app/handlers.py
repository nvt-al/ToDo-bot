import logging

import httpx
from config import CANCEL_EXECUTE, EXECUTE, URI_LIST, URI_TASK, WEB_PARAM
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils import get_task, get_task_list


async def greet_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Called /start")
    name = update.message.from_user.name
    # context.user_data['emoji'] = get_smile(context.user_data)
    # my_keyboard = main_keyboard()
    await update.message.reply_text(f"Здравствуй, {name}!")


async def process_tasks_command(update: Update, _) -> None:
    logging.info("Called /tasks")
    if update.message:
        user_name = update.message.from_user.name
        text, keyboard = get_task_list(user_name)
        await update.message.reply_markdown_v2(text, reply_markup=keyboard)


async def refresh_tasks_list(update: Update, _) -> None:
    if update.callback_query:
        user_name = update.callback_query.from_user.name
        text, keyboard = get_task_list(user_name)
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard)


async def process_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()
    callback = update.callback_query.data
    logging.info(f"Received callback {callback}")
    if callback[: len(URI_TASK)] == URI_TASK:
        await show_task(update, context)
    elif callback == URI_LIST:
        await refresh_tasks_list(update, context)
    elif callback[: len(EXECUTE)] == EXECUTE:
        await execute_task(update, context)
    elif callback[: len(CANCEL_EXECUTE)] == CANCEL_EXECUTE:
        await cancel_execute_task(update, context)


async def show_task(update: Update, _) -> None:
    logging.info("Called show_task")
    user_name = update.callback_query.from_user.name
    uri = update.callback_query.data[len(URI_TASK) :]
    request: dict = httpx.get(uri + WEB_PARAM.format(user_name)).json()
    text, keyboard = get_task(request)
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard)


async def execute_task(update: Update, _) -> None:
    logging.info("called execute_task")
    user_name = update.callback_query.from_user.name
    uri = update.callback_query.data[len(EXECUTE) :]
    request = httpx.put(uri + WEB_PARAM.format(user_name), json={"task_done": True}).json()
    text, keyboard = get_task(request)
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard)


async def cancel_execute_task(update: Update, _) -> None:
    logging.info("called cancel_execute_task")
    user_name = update.callback_query.from_user.name
    uri = update.callback_query.data[len(CANCEL_EXECUTE) :]
    request = httpx.put(uri + WEB_PARAM.format(user_name), json={"task_done": False}).json()
    text, keyboard = get_task(request)
    await update.callback_query.edit_message_text(text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard)
