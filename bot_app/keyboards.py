from config import CANCEL_EXECUTE, EXECUTE, URI_LIST, URI_TASK, Task
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def main_keyboard():
    return ReplyKeyboardMarkup([["/tasks", "/start"]])


def task_list_inline_keyboard(task_list: list[Task]) -> InlineKeyboardMarkup:
    inlinekeyboard = [
        [InlineKeyboardButton(str(i), callback_data=URI_TASK + task.task_uri) for i, task in enumerate(task_list, 1)]
    ]
    return InlineKeyboardMarkup(inlinekeyboard)


def task_inline_keyboard(task: Task) -> InlineKeyboardMarkup:
    if task.task_done:
        key = CANCEL_EXECUTE
        key_txt = "Отменить выполнение"
    else:
        key = EXECUTE
        key_txt = "Выполнить"

    inlinekeyboard = [
        [
            InlineKeyboardButton(key_txt, callback_data=key + task.task_uri),
            InlineKeyboardButton("К списку", callback_data=URI_LIST),
        ]
    ]
    return InlineKeyboardMarkup(inlinekeyboard)
