import feedparser
import requests
import json
from googletrans import Translator
from slugify import slugify

HF_API_KEY = "hf_ВАШ_ТОКЕН"  # можно оставить пустым, если не генерировать картинки
IMG_MODEL = "stabilityai/stable-diffusion-2"

# RSS ленты зарубежных ИИ-новостей
RSS_FEEDS = [
    "https://venturebeat.com/category/ai/feed/",
    "https://www.artificialintelligence-news.com/feed/",
]

translator = Translator()
articles_data = []

print("📡 Получаем новости...")
for feed_url in RSS_FEEDS:
    feed = feedparser.parse(feed_url)
    for entry in feed.entries[:2]:  # берем по 2 новости с каждой ленты
        title_en = entry.title
        summary_en = entry.summary

        # Перевод
        title_ru = translator.translate(title_en, src="en", dest="ru").text
        summary_ru = translator.translate(summary_en, src="en", dest="ru").text

        # Генерация картинки (если есть ключ)
        image_url = ""
        if HF_API_KEY:
            prompt = f"Futuristic AI concept, {title_en}"
            resp = requests.post(
                f"https://api-inference.huggingface.co/models/{IMG_MODEL}",
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                json={"inputs": prompt}
            )
            if resp.status_code == 200:
                image_filename = f"news_{slugify(title_en)}.png"
                with open(image_filename, "wb") as f:
                    f.write(resp.content)
                image_url = image_filename

        articles_data.append({
            "title": title_ru,
            "content": summary_ru,
            "imageUrl": image_url or "default.jpg"
        })

# Сохраняем в news.json
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=2)

print("✅ Новости обновлены!")
