import logging

import config
from handlers import get_context, greet_user, show_tasks_list
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(lineno)d #%(levelname)-8s " "[%(asctime)s] - %(name)s - %(message)s",
)


def main() -> None:
    mybot = Application.builder().token(config.TG_TOKEN).build()

    mybot.add_handler(CommandHandler("start", greet_user))
    mybot.add_handler(CommandHandler("tasks", show_tasks_list))
    mybot.add_handler(CallbackQueryHandler(get_context))

    logging.info("Bot started")
    mybot.run_polling()


if __name__ == "__main__":
    main()
