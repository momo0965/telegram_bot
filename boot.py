from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BOT_TOKEN = '7799327813:AAEnqoNMh-FZHaT8tK0AAwCvfda2RvglTho'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if url.startswith("http://") or url.startswith("https://"):
        await update.message.reply_text("تم استلام الرابط! جاري استخراج الصور...")

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            image_tags = soup.find_all('img')
            image_urls = []

            for img in image_tags:
                src = img.get('src')
                if src:
                    # تصحيح روابط تبدأ بـ //
                    if src.startswith("//"):
                        src = "https:" + src
                    full_url = urljoin(url, src)
                    image_urls.append(full_url)

            if not image_urls:
                await update.message.reply_text("لم يتم العثور على صور في الصفحة.")
            else:
                await update.message.reply_text(f"تم العثور على {len(image_urls)} صورة. يتم الإرسال...")

                print("الصور المستخرجة:")
                for img_url in image_urls:
                    print(img_url)

                for img_url in image_urls:
                    try:
                        await update.message.reply_photo(img_url)
                    except Exception as e:
                        print(f"فشل إرسال الصورة: {img_url} — {e}")

        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء معالجة الرابط:\n{str(e)}")

    else:
        await update.message.reply_text("من فضلك أرسل رابط صحيح يبدأ بـ http:// أو https://")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("البوت يعمل وينتظر روابط صفحات...")
app.run_polling()
