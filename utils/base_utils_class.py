import os
import re
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class PromptAgent:
    def __init__(self, raw_data: dict, id: str):
        self.raw_data = raw_data
        self.id = id
        self.title = raw_data.get("title")
        self.url = raw_data.get("link")

        # self.__scrape_and_clean()

    def __scrape_and_clean(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch content. Status: {response.status_code}")

        soup = BeautifulSoup(response.content, "html.parser")

        body_content = soup.body
        if not body_content:
            raise Exception("Body content not found")

        # Clean up unnecessary tags (e.g., ads, scripts, styles)
        for tag in body_content.find_all(["script", "style", "aside"]):
            tag.decompose()

        raw_html = body_content.get_text(separator="\n", strip=True)
        self.raw_html = raw_html

        # return self.title, raw_html

    def generate_prompt(self):
        self.__scrape_and_clean()
        prompt = f"""
        You are a Prompt Generator. Your task is to generate a prompt for an AI Agent so that it can summarize a technology news article. The output from that AI agent should:
        - Be clear, concise, and engaging.
        - Avoid any ads, unrelated text, or HTML tags.
        - Provide an overview of the news in less than 500 words.
        - Include a call-to-action for readers, such as asking for their opinion.
        Title: {self.title}
        
        Raw HTML Content:
        {self.raw_html}
        
        Desired Output:
        - Just A prompt to pass to an AI agent to generate desired article according to above points from the html provided.
        
        """

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
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
            return content
        else:
            print(f"Error in generation Prompt {response}")

    def get_content(self):
        self.__scrape_and_clean()
        return self.raw_html


class ArticleAgent:
    def __init__(self, prompt, content):
        matches = re.findall(r'"(.*?)"', prompt, re.DOTALL)
        self.prompt = matches[0]
        self.content = content
    
    def generate_article(self):
        prompt = self.prompt + "\n" + self.content
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
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
            self.article = content
            return content
        else:
            print(f"Error in generation Article {response}")