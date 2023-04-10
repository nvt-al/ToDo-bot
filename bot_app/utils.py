import httpx
from config import EMOJI_DONE, EMOJI_TODO, WEB, WEB_PARAM, Task
from emoji import emojize
from keyboards import task_inline_keyboard, task_list_inline_keyboard


def get_text_tasks(task_list: list[Task]) -> str:
    text: str = "Задачи на сегодня:\n\n"
    for index, task in enumerate(task_list, start=1):
        text += str(index)
        # time = task.get('time', '')
        if task.task_done:
            text += f' {emojize(EMOJI_DONE, language="alias")} ~{task.name}~\n'
        else:
            text += f' {emojize(EMOJI_TODO, language="alias")} {task.name}\n'
    text += "\nВыберите номер задачи для просмотра"
    return text


def get_text_task(task: Task) -> str:
    text: str = f"*{task.name}*\n\n"
    if task.task_done:
        text += f' {emojize(EMOJI_DONE, language="alias")} Завершено\n'
    else:
        text += f' {emojize(EMOJI_TODO, language="alias")} Выполнить\n'
    # text += f"Время \- {task.get('time', 'Не задано')}\n"
    text += f"{task.description}"
    return text


def get_task_list(user: str):
    request: dict = httpx.get(WEB + WEB_PARAM.format(user)).json()
    error = request.get("error")
    if not error:
        task_list: list[Task] = [Task(**task) for task in request["tasks"]]
        text = get_text_tasks(task_list)
        keyboard = task_list_inline_keyboard(task_list)
    else:
        text = error
        keyboard = None
    return (text, keyboard)


def get_task(request):
    error = request.get("error")
    if not error:
        task: Task = Task(**request["task"])
        text = get_text_task(task)
        keyboard = task_inline_keyboard(task)
    else:
        text = error
        keyboard = None
    return (text, keyboard)
