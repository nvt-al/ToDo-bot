from telegram.ext import ContextTypes


async def send_hello(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=1329139903, text="Привет")
