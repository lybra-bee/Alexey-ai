import os
import requests
import json
from datetime import datetime

# Получаем ключ API из переменных окружения
API_KEY = os.getenv("NEWS_API_KEY")
if not API_KEY:
    raise ValueError("❌ NEWS_API_KEY не найден! Добавь его в GitHub Secrets или .env файл.")

NEWS_URL = "https://newsapi.org/v2/everything"
QUERY = "artificial intelligence"
LANGUAGE = "en"
PAGE_SIZE = 5

OUTPUT_FILE = "news.json"

def get_ai_news():
    params = {
        "q": QUERY,
        "language": LANGUAGE,
        "sortBy": "publishedAt",
        "pageSize": PAGE_SIZE,
        "apiKey": API_KEY
    }
    r = requests.get(NEWS_URL, params=params)
    r.raise_for_status()
    data = r.json()
    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a["title"],
            "content": a["description"] or "",
            "url": a["url"],
            "imageUrl": a["urlToImage"] or ""
        })
    return articles

def save_news(articles):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    print(f"[{datetime.now()}] Запуск генерации новостей...")
    news = get_ai_news()
    save_news(news)
    print(f"✅ Сохранено {len(news)} новостей в {OUTPUT_FILE}")
