import feedparser
import requests
from deep_translator import GoogleTranslator
import time
from datetime import datetime

BOT_TOKEN = "8651602237:AAF-YUYTpPoi9QGPGN9iRgT5dkRKABYMkAU"
CHAT_ID = "-5104075619"

RSS_FEEDS = {
    "🇺🇸 Reuters": "https://feeds.reuters.com/reuters/topNews",
    "🇺🇸 AP News": "https://feeds.apnews.com/apnews/TopNews",
    "🇮🇱 Times of Israel": "https://www.timesofisrael.com/feed/",
    "🇮🇷 Tehran Times": "https://www.tehrantimes.com/rss",
}

KEYWORDS = ["iran","america","usa","israel","israeli","iranian",
            "tehran","washington","tel aviv","netanyahu","trump",
            "nuclear","middle east","Gaza","Hamas","Hezbollah"]

translator = GoogleTranslator(source='auto', target='ar')
sent_links = set()

def translate_text(text):
    try:
        return translator.translate(text[:500])
    except:
        return text

def is_relevant(title, summary=""):
    content = (title + " " + summary).lower()
    return any(kw.lower() in content for kw in KEYWORDS)

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    requests.post(url, json=payload)

def fetch_and_send():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] جاري جلب الأخبار...")
    count = 0
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = entry.get('title', '')
                link = entry.get('link', '')
                summary = entry.get('summary', '')
                if link in sent_links:
                    continue
                if is_relevant(title, summary):
                    ar_title = translate_text(title)
                    ar_summary = translate_text(summary[:300]) if summary else ""
                    message = f"{source}\n━━━━━━━━━━━━━━━━━\n📰 <b>{ar_title}</b>\n\n📝 {ar_summary}\n\n🔗 <a href='{link}'>اقرأ الخبر</a>\n🕐 {datetime.now().strftime('%H:%M')}"
                    send_to_telegram(message)
                    sent_links.add(link)
                    count += 1
                    time.sleep(2)
        except Exception as e:
            print(f"خطأ: {e}")
    print(f"✅ تم إرسال {count} خبر")

send_to_telegram("🤖 <b>البوت شغال!</b>")
while True:
    fetch_and_send()
    print("⏳ انتظار 30 دقيقة...")
    time.sleep(30)

