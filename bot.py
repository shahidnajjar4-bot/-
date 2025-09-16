import os
import random
import time
import logging
from flask import Flask
from threading import Thread
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# تخزين الألعاب الجارية
games = {}

# دوال أوامر البوت
def start_cmd(update, context):
    update.message.reply_text("أهلاً بك في لعبة الروليت! أرسل /newgame لبدء لعبة جديدة.")

def newgame_cmd(update, context):
    chat_id = update.effective_chat.id
    if chat_id in games:
        update.message.reply_text("هناك لعبة جارية بالفعل.")
        return
    games[chat_id] = []
    update.message.reply_text("بدأت لعبة روليت جديدة! أرسل اسمك أو اضغط /players لرؤية المشاركين.")

def players_cmd(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in games or len(games[chat_id]) == 0:
        update.message.reply_text("لا يوجد لاعبين بعد.")
    else:
        names = "\n".join(games[chat_id])
        update.message.reply_text(f"اللاعبون:\n{names}")

# هنا ضع منطق لعبتك … (هذا مثال بسيط)
# …

# إعداد التوكن من Environment
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("ضع BOT_TOKEN في Environment Variables على Render.")

# إعداد التليجرام
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# إضافة أوامر
dp.add_handler(CommandHandler("start", start_cmd))
dp.add_handler(CommandHandler("newgame", newgame_cmd))
dp.add_handler(CommandHandler("players", players_cmd))
# يمكنك إضافة المزيد من الأوامر هنا

# تطبيق Flask لتشغيله على Render
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # تشغيل Flask في Thread جانبي
    Thread(target=run_flask).start()

    # تشغيل البوت باستخدام Webhook بدلاً من Polling
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get('PORT', 10000)),
        url_path=TOKEN
    )

    # هنا ضع رابط تطبيقك على Render
    updater.bot.set_webhook("https://اسم-تطبيقك.onrender.com/" + TOKEN)

    updater.idle()