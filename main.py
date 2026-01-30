import os
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start(update, context):
    await update.message.reply_text("The system is online.")

app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run_polling()
