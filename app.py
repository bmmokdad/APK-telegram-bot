import telebot
from flask import Flask, request

API_TOKEN = '7565366701:AAHX-tPCdUA8w6PEWYsKNZUWX2lF11Jui3Q'
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# تخزين حالة المستخدم إذا كان بوضع البحث
user_search_mode = {}

# أقسام التطبيقات وروابطها
apps_by_category = {
    "مونتاج فيديو": [
        ("KineMaster Pro", "https://example.com/kine.apk"),
        ("CapCut مهكر", "https://example.com/capcut.apk")
    ],
    "تعديل صور": [
        ("PicsArt Gold", "https://example.com/picsart.apk"),
        ("Lightroom Premium", "https://example.com/lightroom.apk")
    ],
    "ألعاب مهكرة": [
        ("Subway مهكرة", "https://example.com/subway.apk"),
        ("GTA San Andreas", "https://example.com/gta.apk")
    ],
    "متصفحات": [
        ("UC Browser", "https://example.com/uc.apk"),
        ("Brave مهكر", "https://example.com/brave.apk")
    ],
    "أدوات الهاتف": [
        ("SD Maid Pro", "https://example.com/sdmaid.apk"),
        ("Greenify", "https://example.com/greenify.apk")
    ],
    "تطبيقات تواصل مطورة": [
        ("WhatsApp Gold", "https://example.com/whatsappgold.apk"),
        ("Telegram X", "https://example.com/telegramx.apk")
    ]
}

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_search_mode[message.chat.id] = False  # إعادة تعيين وضع البحث
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(telebot.types.KeyboardButton("🔍 بحث عن تطبيق مهكّر"))
    markup.add(telebot.types.KeyboardButton("مونتاج فيديو"))
    markup.add(telebot.types.KeyboardButton("تعديل صور"))
    markup.add(telebot.types.KeyboardButton("ألعاب مهكرة"))
    markup.add(telebot.types.KeyboardButton("متصفحات"))
    markup.add(telebot.types.KeyboardButton("أدوات الهاتف"))
    markup.add(telebot.types.KeyboardButton("تطبيقات تواصل مطورة"))
    markup.add(telebot.types.KeyboardButton("مساعدة"))

    bot.send_message(
        message.chat.id,
        "أهلًا في بوت التطبيقات المهكّرة 🌚\nاختر نوع التطبيقات أو اضغط عالبحث لتدوّر على تطبيق محدد:",
        reply_markup=markup
    )

# رسائل عامة
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    # إذا كبس بحث
    if text == "🔍 بحث عن تطبيق مهكّر":
        user_search_mode[chat_id] = True
        bot.send_message(chat_id, "اكتبلي اسم التطبيق يلي بدك تهكّرو 🌚")
        return

    # إذا كان بحالة البحث
    if user_search_mode.get(chat_id, False):
        formatted = text.replace(" ", "_").lower()
        link = f"https://example.com/downloads/{formatted}.apk"
        user_search_mode[chat_id] = False  # رجّعو للوضع العادي
        bot.send_message(chat_id, f"دورتلك على **{text}**، جرب حمّلو من هون:\n{link}", parse_mode="Markdown")
        return

    # إذا اختار قسم من الأقسام
    if text in apps_by_category:
        response = f"أفضل تطبيقات قسم **{text}**:\n\n"
        for name, link in apps_by_category[text]:
            response += f"• [{name}]({link})\n"
        bot.send_message(chat_id, response, parse_mode="Markdown")
        return

    # مساعدة
    if text == "مساعدة":
        bot.send_message(chat_id, "استخدم الأزرار لتتصفح الأقسام، أو اضغط على 🔍 لتدوّر على تطبيق معيّن.")
        return

    # أي شي مو معروف
    bot.send_message(chat_id, "ما فهمت عليك، اختار من الأزرار تحت أو جرب تكتب اسم تطبيق.")

# Webhook
@app.route('/', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route('/')
def index():
    return "بوت التطبيقات شغّال يملك 🌚"

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url='https://apk-telegram-bot.onrender.com')
    app.run(host='0.0.0.0', port=5000)
