import logging
from datetime import datetime

import httpx
from config import WEB, Task
from keyboards import task_inline_keyboard
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from utils import get_text_task


async def send_notification(context: ContextTypes.DEFAULT_TYPE):
    logging.info("send hello")
    time: str = datetime.now().strftime("%H:%M")
    request: dict = httpx.get(WEB + "time/" + time).json()
    error = request.get("error")
    if not error:
        task_list: list[Task] = [Task(**task) for task in request["tasks"]]
        for task in task_list:
            text = get_text_task(task)
            keyboard = task_inline_keyboard(task)
            await context.bot.send_message(
                chat_id=task.telegram_id, text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=keyboard
            )
    else:
        logging.info("error {error}")
