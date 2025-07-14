from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import undetected_chromedriver as uc
import time
import os

# توكن البوت من متغير البيئة
TOKEN = os.environ.get("8185073049:AAEY7SPjWPE9bYIo2zZ4OvYEw0zAAVFxWkw")

ASK_CREDENTIALS = 1

def start(update, context):
    update.message.reply_text("اكتب /login علشان تسجل دخولك على OkCupid")

def login(update, context):
    update.message.reply_text("ابعت الإيميل والباسورد بالشكل ده:\n`email:password`")
    return ASK_CREDENTIALS

def get_credentials(update, context):
    try:
        text = update.message.text.strip()
        email, password = text.split(':', 1)
        update.message.reply_text("🔄 جاري تسجيل الدخول...")

        options = uc.ChromeOptions()
        options.headless = True
        driver = uc.Chrome(options=options)

        driver.get("https://okcupid.com/login")
        time.sleep(5)

        email_input = driver.find_element("name", "username")
        password_input = driver.find_element("name", "password")
        email_input.send_keys(email)
        password_input.send_keys(password)

        login_btn = driver.find_element("xpath", "//button[@type='submit']")
        login_btn.click()

        time.sleep(7)

        if "okcupid.com/doubletake" in driver.current_url or "okcupid.com/profile" in driver.current_url:
            update.message.reply_text("✅ تم تسجيل الدخول بنجاح!")
        elif "login" in driver.current_url:
            update.message.reply_text("❌ فشل تسجيل الدخول. تأكد من البيانات.")
        else:
            update.message.reply_text(f"⚠️ حالة غير متوقعة: {driver.current_url}")

        driver.quit()

    except Exception as e:
        update.message.reply_text(f"🚫 حصل خطأ: {str(e)}")
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

updater = Updater(TOKEN)
dp = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('login', login)],
    states={ASK_CREDENTIALS: [MessageHandler(Filters.text & ~Filters.command, get_credentials)]},
    fallbacks=[CommandHandler('cancel', cancel)],
)

dp.add_handler(CommandHandler('start', start))
dp.add_handler(conv_handler)

updater.start_polling()
updater.idle()
