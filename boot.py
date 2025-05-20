import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# قراءة توكن البوت من متغير البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if url.startswith("http://") or url.startswith("https://"):
        await update.message.reply_text("تم استلام الرابط! جاري استخراج الصور...")

        try:
            # جلب محتوى الصفحة
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # استخراج كل روابط الصور <img src="...">
            image_tags = soup.find_all('img')
            image_urls = []

            for img in image_tags:
                src = img.get('src')
                if src:
                    full_url = urljoin(url, src)  # لحل الروابط النسبية
                    image_urls.append(full_url)

            if not image_urls:
                await update.message.reply_text("لم يتم العثور على صور في الصفحة.")
            else:
                await update.message.reply_text(f"تم العثور على {len(image_urls)} صورة. يتم الإرسال...")

                # إرسال جميع الصور (يمكن تعديل العدد حسب الحاجة)
                for img_url in image_urls:
                    await update.message.reply_photo(img_url)

        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء معالجة الرابط:\n{str(e)}")

    else:
        await update.message.reply_text("من فضلك أرسل رابط صحيح يبدأ بـ http:// أو https://")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("البوت يعمل وينتظر روابط صفحات...")
app.run_polling()
