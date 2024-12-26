import os
import uuid
import requests
from dotenv import load_dotenv
from nodes.state_manager import CustomState, graph

load_dotenv()


NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")



def filter_tech_articles(state: CustomState):
    print("###################### filter #########################")
    if state.articles:
        titles = [{"id": article["id"], "title": article["title"]} for article in state.articles]
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
            filtered_articles = []
            for article in state.articles:
                for ids_string in filtered_ids:
                    if article["id"] in ids_string:
                        filtered_articles.append(article)
            if len(filtered_articles) != 0:
                state.filtered_articles = filtered_articles
                state.state_stack.append("store_news_in_dynamodb")
            else:
                state.state_stack.pop()
            return {"filtered_articles": filtered_articles}
        else:
            print(f"Error filtering with AI: {response.status_code} - {response.text}")
            if len(state.state_stack) > 0:
                state.state_stack.pop()
            return {}
