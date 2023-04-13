import logging

import config
from handlers import greet_user, process_callback, process_tasks_command
from jobs import send_notification
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(lineno)d #%(levelname)-8s " "[%(asctime)s] - %(name)s - %(message)s",
)


def main() -> None:
    mybot = Application.builder().token(config.TG_TOKEN).build()

    jq = mybot.job_queue
    jq.run_repeating(send_notification, interval=60)

    mybot.add_handler(CommandHandler("start", greet_user))
    mybot.add_handler(CommandHandler("tasks", process_tasks_command))
    mybot.add_handler(CallbackQueryHandler(process_callback))

    logging.info("Bot started")
    mybot.run_polling()


if __name__ == "__main__":
    main()
