import os
import requests
from flask import Flask, request

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://xxx.up.railway.app/telegram

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("Missing BOT_TOKEN or WEBHOOK_URL")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)

# 設定 webhook（每次啟動都 set 一次，最穩）
def set_webhook():
    r = requests.get(f"{API}/setWebhook", params={"url": WEBHOOK_URL})
    print("setWebhook:", r.status_code, r.text)

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = request.get_json(force=True)

    # 最簡單測試：收到任何訊息就回覆 "OK"
    message = update.get("message")
    if message and "chat" in message:
        chat_id = message["chat"]["id"]
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id,
            "text": "✅ Webhook received. Bot is working."
        })

    return "ok", 200

@app.route("/", methods=["GET"])
def health():
    return "alive", 200

if __name__ == "__main__":
    set_webhook()
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
