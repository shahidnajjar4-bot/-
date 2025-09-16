from telegram.ext import Updater, CommandHandler
from telegram import InputFile
from flask import Flask, request
import logging
import os

# إعداد اللوجز لتسهيل معرفة الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# توكن البوت من متغير البيئة
TOKEN = os.environ.get("BOT_TOKEN")

# إعداد Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json(force=True)
    updater.dispatcher.process_update(
        updater.bot._update_class.de_json(update, updater.bot)
    )
    return 'ok'

# أوامر البوت
def start(update, context):
    update.message.reply_text("اهلا! البوت يعمل بنجاح 🎉")

def help_command(update, context):
    update.message.reply_text("هذا أمر المساعدة.")

# إعداد الـ Updater
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# إضافة الأوامر
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))

# تشغيل البوت
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    if os.environ.get('RENDER'):
        # وضع الـ webhook عند التشغيل على Render
        updater.bot.set_webhook(f"https://roulette-bot.onrender.com/{TOKEN}")
        app.run(host='0.0.0.0', port=PORT)
    else:
        # تشغيل البوت في Termux (polling)
        updater.start_polling()
        updater.idle()
