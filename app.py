import telebot
from flask import Flask, request

API_TOKEN = '7565366701:AAHX-tPCdUA8w6PEWYsKNZUWX2lF11Jui3Q'  # توكن البوت
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# الرد على /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton("أرسل اسم التطبيق المهكّر")
    btn2 = telebot.types.KeyboardButton("مساعدة")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "أهلًا وسهلًا في بوت التطبيقات المهكّرة 🌚\nاكتب اسم التطبيق يلي بدك ياه:", reply_markup=markup)

# استقبال أي رسالة نصية (اسم التطبيق)
@bot.message_handler(func=lambda message: True)
def app_request(message):
    app_name = message.text.strip()
    
    if app_name == "مساعدة":
        bot.reply_to(message, "اكتب اسم أي تطبيق مهكّر بدك تحملو، وأنا ببعتلك رابطو مباشرة إذا متوفر 🌚")
        return

    # رد تجريبي - لاحقًا نربطه بقواعد بيانات وروابط
    download_url = f"https://example.com/downloads/{app_name.replace(' ', '_')}.apk"
    bot.send_message(message.chat.id, f"لقيتلك تطبيق {app_name}، حملو من هون:\n{download_url}")

# إعداد Flask للبوت على Render
@app.route('/', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@app.route('/')
def index():
    return "بوت التطبيقات شغال تمام!"

# إعداد Webhook
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://apk-telegram-bot.onrender.com')  # رابط الريندر
    app.run(host='0.0.0.0', port=5000)if __name__ == "__main__":
    bot.remove_webhook()  # إزالة أي Webhook قديم
    bot.set_webhook(url="https://apk-telegram-bot.onrender.com/7565366701:AAHX-tPCdUA8w6PEWYsKNZUWX2lF11Jui3Q")  # تعيين الـ Webhook الجديد
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
