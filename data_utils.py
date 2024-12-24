import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()


NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def fetch_tech_news():
    # url = "https://newsdata.io/api/1/news"
    nurl = "https://newsdata.io/api/1/latest"
    params = {"apikey": NEWS_API_KEY,"category": "technology", "language": "en"}
    response = requests.get(nurl, params=params)
    if response.status_code == 200:
        articles = response.json().get("results", [])
        return [{"id": str(uuid.uuid4()), **article} for article in articles]
    else:
        print(f"Error fetching news: {response.status_code}")
        return []


def filter_tech_articles(articles):
    titles = [{"id": article["id"], "title": article["title"]} for article in articles]
    prompt = (
        "Filter the following list of article titles and IDs. "
        "Return only the IDs of titles related to technology advancements, AI, cloud, or emerging tech:\n\n"
        + "\n".join([f"{item['id']}: {item['title']}" for item in titles])
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}",
    }

    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
    )

    if response.status_code == 200:
        ai_response = response.json()
        content = ai_response["choices"][0]["message"]["content"]
        filtered_ids = [line.strip() for line in content.split("\n") if line.strip()]
        return filtered_ids
    else:
        print(f"Error filtering with AI: {response.status_code} - {response.text}")
        return []
