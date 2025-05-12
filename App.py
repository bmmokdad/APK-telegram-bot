import telebot
from flask import Flask, request

API_TOKEN = '7565366701:AAHX-tPCdUA8w6PEWYsKNZUWX2lF11Jui3Q'
bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

# قاعدة بيانات بسيطة للتطبيقات
apps_links = {
    "inshot": "https://example.com/inshot_pro.apk",
    "spotify": "https://example.com/spotify_premium.apk",
    "picsart": "https://example.com/picsart_gold.apk"
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلًا وسهلًا ببوت التطبيقات المهكرة 🌚\nاكتبلي اسم التطبيق يلي بدك تنزلو.")

@bot.message_handler(func=lambda message: True)
def handle_app_request(message):
    app_name = message.text.lower()
    if app_name in apps_links:
        bot.reply_to(message, f"رابط مباشر لتحميل {app_name}:\n{apps_links[app_name]}")
    else:
        bot.reply_to(message, "ما لقيت هالتطبيق عندي 💔\nجرب اسم تاني، أو ابعتلي اقتراح.")

@server.route(f"/{API_TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

@server.route("/")
def index():
    return "البوت شغال تمام 🌐"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"https://your-render-app-name.onrender.com/{API_TOKEN}")
    server.run(host="0.0.0.0", port=5000)
