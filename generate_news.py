import json
import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")
MODEL = "gpt2"  # Можно заменить на ruGPT или другую модель

def generate_article(topic):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": f"Напиши новость про {topic} на русском языке."}
    r = requests.post(f"https://api-inference.huggingface.co/models/{MODEL}", headers=headers, json=payload)
    text = r.json()[0]["generated_text"]

    return {
        "title": topic,
        "content": text,
        "imageUrl": f"https://via.placeholder.com/800x400?text={topic.replace(' ', '+')}"
    }

topics = ["ИИ", "Робототехника", "Нейросети", "OpenAI", "Космос и технологии"]

news = [generate_article(t) for t in topics]

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news, f, ensure_ascii=False, indent=2)
