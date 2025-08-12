import os
import json
import requests
import feedparser
from datetime import datetime
from pathlib import Path
import base64

# === НАСТРОЙКИ ===
NEWS_JSON = "news.json"
IMAGES_DIR = Path("images/news")
HF_API_KEY = os.getenv("HF_API_KEY")  # ключ в GitHub Secrets
NEWS_FEED = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en&gl=US&ceid=US:en"
ARTICLES_LIMIT = 5

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def fetch_foreign_news():
    feed = feedparser.parse(NEWS_FEED)
    return feed.entries[:ARTICLES_LIMIT]

def translate_and_rewrite(text):
    url = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
    payload = {"inputs": f"Переведи и перескажи по-русски: {text}"}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        data = resp.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
    except Exception as e:
        print("Ошибка перевода:", e)
    return text  # если не получилось — вернём оригинал

def generate_image(prompt, filename):
    url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"} if HF_API_KEY else {}
    try:
        resp = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=120)
        if resp.status_code == 200:
            with open(filename, "wb") as f:
                f.write(resp.content)
            return str(filename)
        else:
            print("Ошибка генерации картинки:", resp.text)
    except Exception as e:
        print("Ошибка запроса картинки:", e)
    return None

def main():
    news_entries = fetch_foreign_news()
    articles = []

    for i, entry in enumerate(news_entries, start=1):
        title = translate_and_rewrite(entry.title)
        summary = translate_and_rewrite(entry.summary)
        img_filename = IMAGES_DIR / f"news_{i}.png"
        image_path = generate_image(title, img_filename)

        articles.append({
            "title": title,
            "content": summary,
            "imageUrl": image_path if image_path else "images/placeholder.png",
            "date": datetime.utcnow().isoformat()
        })

    with open(NEWS_JSON, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Сохранено {len(articles)} статей")

if __name__ == "__main__":
    main()
