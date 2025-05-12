import telebot
from flask import Flask, request

API_TOKEN = '7565366701:AAHX-tPCdUA8w6PEWYsKNZUWX2lF11Jui3Q'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# أمر /start مع كيبورد عربي
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("أرسل اسم التطبيق المهكّر")
    btn2 = telebot.types.KeyboardButton("مساعدة")
    markup.add(btn1, btn2)
    bot.send_message(
        message.chat.id,
        "أهلًا وسهلًا في بوت التطبيقات المهكّرة 🌚\nاكتب اسم التطبيق يلي بدك ياه:",
        reply_markup=markup
    )

# أي رسالة نصية (اسم تطبيق)
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    app_name = message.text.strip()

    if app_name == "مساعدة":
        bot.reply_to(
            message,
            "اكتب اسم أي تطبيق مهكّر بدك تحملو، وأنا ببعتلك رابطو مباشرة إذا متوفر 🌚"
        )
        return

    # رابط تجريبي حسب اسم التطبيق
    download_url = f"https://example.com/downloads/{app_name.replace(' ', '_')}.apk"
    bot.send_message(
        message.chat.id,
        f"لقيتلك تطبيق {app_name}، حملو من هون:\n{download_url}"
    )

# Webhook لاستقبال التحديثات من Telegram
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# صفحة بسيطة لعرض حالة البوت
@app.route('/')
def index():
    return "بوت التطبيقات شغال تمام!"

# تشغيل البوت وتعيين الـ webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://apk-telegram-bot.onrender.com')
    app.run(host='0.0.0.0', port=5000)
