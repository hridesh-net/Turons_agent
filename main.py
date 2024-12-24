import os
from dotenv import load_dotenv

from base_utils_class import PromptAgent, ArticleAgent
from data_utils import fetch_tech_news, filter_tech_articles
from aws_utils import update_article_in_dynamodb, store_news_in_dynamodb

load_dotenv()

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "TechNews")



if __name__ == "__main__":
    print("Fetching tech news...")
    articles = fetch_tech_news()
    print("-------------------")
    print(articles)
    print(f"Fetched {len(articles)} articles. Sending to AI for filtering...")

    # Send to AI agent for filtering
    filtered_ids = filter_tech_articles(articles)
    print("-------------------")
    print(filtered_ids)
    filtered_articles = []
    for article in articles:
        for ids_string in filtered_ids:
            if article["id"] in ids_string:
                filtered_articles.append(article)
    print(f"AI filtered {len(filtered_ids)} articles.")

    if filtered_articles:
        print("Storing filtered articles in DynamoDB...")
        store_news_in_dynamodb(filtered_articles)
        for article in filtered_articles:
            try:
                prompt = PromptAgent(article, article.get("id"))
                prompt_text = prompt.generate_prompt()
                content = prompt.get_content()
                newsletter = ArticleAgent(prompt_text, content)
                news_article = newsletter.generate_article()
                update_article_in_dynamodb(article.get("id"), news_article)
            except Exception as e:
                print(e)
                continue
            print("Done!")
    else:
        print("No tech articles found.")
