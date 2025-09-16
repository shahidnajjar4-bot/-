from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InputFile, InlineKeyboardButton, InlineKeyboardMarkup, Update
from flask import Flask, request
import logging
import imghdr  # بدل imgdhr
import os

# تفعيل اللوجز لمعرفة الأخطاء
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# ضع توكن البوت هنا
TOKEN = os.environ.get("BOT_TOKEN") or "ضع_التوكن_هنا"

# إعدادات Flask
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json(force=True)
    updater.dispatcher.process_update(
        Update.de_json(update, updater.bot)
    )
    return 'ok'

# أوامر البوت
def start(update, context):
    update.message.reply_text("أهلاً! البوت يعمل بنجاح 🎉")

def help_command(update, context):
    update.message.reply_text("هذا أمر المساعدة.")

# إعداد Updater
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# إضافة الهاندلرز
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))

# التشغيل المحلي (بدون ويب هوك)
if __name__ == "__main__":
    # إذا كنا على Render نستخدم ويب هوك
    PORT = int(os.environ.get('PORT', 5000))
    if os.environ.get('RENDER'):
        updater.bot.set_webhook(f"https://roulette-bot.onrender.com/{TOKEN}")
        app.run(host='0.0.0.0', port=PORT)
    else:
        # للتشغيل على جهازك أو Termux
        updater.start_polling()
        updater.idle()
