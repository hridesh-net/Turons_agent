import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.logging import RichHandler
import logging

from utils.base_utils_class import PromptAgent, ArticleAgent
from utils.data_utils import fetch_tech_news, filter_tech_articles
from utils.aws_utils import update_article_in_dynamodb, store_news_in_dynamodb

load_dotenv()

console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)

logger = logging.getLogger("turons_logger")

def log_boxed_message(title, message):
    box = Panel(message, title=title, expand=False, border_style="bold green")
    console.print(box)

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "TechNews")



if __name__ == "__main__":
    logger.info("Starting application...")
    log_boxed_message("INFO", "Fetching tech news...")
    log_boxed_message("SUCCESS", "Successfully stored articles in DynamoDB!")
    log_boxed_message("INFO", "🌐 Fetching tech news...")
    articles = fetch_tech_news()
    logger.info("-------------------")
    log_boxed_message("INFO", f"📋 Fetched articles: {articles}")
    log_boxed_message("INFO", f"📚 Fetched {len(articles)} articles. Sending to AI for filtering...")

    # Send to AI agent for filtering
    filtered_ids = filter_tech_articles(articles)
    logger.info("-------------------")
    log_boxed_message("INFO", f"🎯 Filtered IDs: {filtered_ids}")
    
    filtered_articles = []
    for article in articles:
        for ids_string in filtered_ids:
            if article["id"] in ids_string:
                filtered_articles.append(article)
    log_boxed_message("INFO", f"🤖 AI filtered {len(filtered_ids)} articles.")

    if filtered_articles:
        log_boxed_message("INFO", "💾 Storing filtered articles in DynamoDB...")
        store_news_in_dynamodb(filtered_articles)
        for article in filtered_articles:
            try:
                prompt = PromptAgent(article, article.get("id"))
                prompt_text = prompt.generate_prompt()
                content = prompt.get_content()
                newsletter = ArticleAgent(prompt_text, content)
                news_article = newsletter.generate_article()
                update_article_in_dynamodb(article.get("id"), news_article)
                log_boxed_message("SUCCESS", f"✅ Article ID {article.get('id')} processed successfully.")
            except Exception as e:
                log_boxed_message("ERROR", f"❌ Error processing article {article.get('id')}: {e}")
                continue

    else:
        log_boxed_message("WARNING", "⚠️ No tech articles found.")
