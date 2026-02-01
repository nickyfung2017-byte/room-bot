import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


BOT_TOKEN = os.environ["BOT_TOKEN"]
PUBLIC_URL = os.environ["PUBLIC_URL"]  # 例如 https://room-bot-production-3743.up.railway.app
WEBHOOK_PATH = os.environ.get("WEBHOOK_PATH", "telegram")  # 可唔填，預設 telegram


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ The system is online.")


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🏓 pong")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))

    port = int(os.environ.get("PORT", "8080"))
    webhook_url = f"{PUBLIC_URL}/{WEBHOOK_PATH}".rstrip("/")

    # Railway: 用 webhook，不要用 run_polling
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=WEBHOOK_PATH,
        webhook_url=webhook_url,
        drop_pending_updates=True,
        allowed_updates=["message", "channel_post"],
    )


if __name__ == "__main__":
    main()
