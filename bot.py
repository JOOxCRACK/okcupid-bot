import os
import json
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

TOKEN = os.environ.get("TOKEN")
ASK_CREDENTIALS = 1

HEADERS = {
    "Host": "e2p-okapi.api.okcupid.com",
    "x-okcupid-platform": "ios",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjb3JlYXBpIiwiYXVkIjoiY29yZWFwaSIsInBsYXRmb3JtSWQiOjExMSwic2Vzc2lvbklkIjoiODMxMDUwN2QtNDA3Ni00ZDMyLTkyODMtNTZkYTUyM2Y1NTVlIiwic2l0ZUNvZGUiOjM2LCJTZXJ2ZXJJZCI6NzgsInZlciI6MTIsImlzc1NyYyI6MjcsImVudiI6MSwic2NvcGUiOlsxXSwiYXV0aF90aW1lIjpudWxsLCJpYXQiOjE3NTI0OTMyMTEsImV4cCI6MTc1MjQ5NTkxMX0.z2zF6XN6UVrq_oMX6-s-XVIm9WgDzmPs2qJpscrw1V4",  # لو مش ضروري شيله أو حدّثه
    "x-okcupid-locale": "en",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "x-okcupid-auth-v": "1",
    "x-match-useragent": "OkCupid/103.1.0 iOS/18.5",
    "x-okcupid-version": "103.1.0",
    "User-Agent": "OkCupid/103.1.0 iOS/18.5",
    "X-APOLLO-OPERATION-TYPE": "mutation",
    "apollographql-client-name": "com.okcupid.app-apollo-ios",
    "x-okcupid-device-id": "25D8E807-E745-46F5-9BF4-FF92AF8C14EE",
    "X-APOLLO-OPERATION-NAME": "authEmailLogin"
}

def start(update, context):
    update.message.reply_text("اكتب /login وانا هسجلك في OkCupid")

def login(update, context):
    update.message.reply_text("ابعت الإيميل والباسورد كده:\n`email:password`")
    return ASK_CREDENTIALS

def get_credentials(update, context):
    try:
        message = update.message.text.strip()
        email, password = message.split(":", 1)
        update.message.reply_text("⏳ جاري تسجيل الدخول...")

        payload = {
            "operationName": "authEmailLogin",
            "query": "mutation authEmailLogin($input: AuthEmailLoginInput!) { authEmailLogin(input: $input) { __typename encryptedUserId status token } }",
            "variables": {
                "input": {
                    "email": email,
                    "password": password
                }
            }
        }

        response = requests.post(
            "https://e2p-okapi.api.okcupid.com/graphql?operationName=authEmailLogin",
            headers=HEADERS,
            data=json.dumps(payload)
        )

        data = response.json()
        if data.get("data") and data["data"].get("authEmailLogin") and data["data"]["authEmailLogin"]["status"] == "SUCCESS":
            update.message.reply_text("✅ تم تسجيل الدخول بنجاح!\nToken: " + data["data"]["authEmailLogin"]["token"])
        else:
            update.message.reply_text("❌ فشل تسجيل الدخول. البيانات غير صحيحة أو تم حظرك.")
    except Exception as e:
        update.message.reply_text(f"🚫 حصل خطأ: {str(e)}")

    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("تم الإلغاء.")
    return ConversationHandler.END

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_poin_
