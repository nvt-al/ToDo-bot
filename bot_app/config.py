import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

TG_TOKEN = os.getenv("TG_TOKEN", "")

WEB = "http://127.0.0.1:5000/todo/api/v1.0/tasks/"
WEB_PARAM = "?telegram={}"


EMOJI_TODO = ":white_medium_square:"
EMOJI_DONE = ":white_check_mark:"

EXECUTE = "EXECUTE"
CANCEL_EXECUTE = "CANCEL_EXECUTE"
ON_TASK = "ON_TASK"
OFF_TASK = "OFF_TASK"
URI_TASK = "URI_TASK"
URI_LIST = "URI_LIST"


@dataclass
class Task:
    task_uri: str
    template_uri: str
    name: str
    description: str
    telegram_id: int | None = None
    time: str | None = None
    is_active: bool | None = None
    task_done: bool | None = None
