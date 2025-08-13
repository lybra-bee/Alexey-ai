import requests, json, os
from datetime import datetime
from googletrans import Translator
from PIL import Image
from io import BytesIO

HF_API_KEY = os.getenv("HF_API_KEY")
NEWS_FILE = "news.json"

translator = Translator()

def get_ai_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "artificial intelligence",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": "demo"  # тут можно вставить свой бесплатный API ключ newsapi.org
    }
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()["articles"]

def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    data = {"inputs": prompt}
    r = requests.post("https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2", headers=headers, json=data)
    if r.status_code == 200:
        img = Image.open(BytesIO(r.content))
        filename = f"news_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        img.save(filename)
        return filename
    return None

def main():
    articles = get_ai_news()
    news_data = []
    for art in articles:
        title_ru = translator.translate(art["title"], src="en", dest="ru").text
        desc_ru = translator.translate(art["description"] or "", src="en", dest="ru").text
        image_path = generate_image(title_ru) or art.get("urlToImage", "")
        news_data.append({
            "title": title_ru,
            "content": desc_ru,
            "imageUrl": image_path,
            "sourceUrl": art["url"],
            "publishedAt": art["publishedAt"]
        })
    with open(NEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
