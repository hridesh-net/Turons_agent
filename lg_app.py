import os
import uuid
import requests
from dotenv import load_dotenv
from typing import Annotated, Literal, TypedDict

# from nodes.filter_tech_article
from nodes.state_manager import State
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState, state
from langgraph.prebuilt import ToolNode

from nodes.db_node import *
from nodes.state_manager import graph, CustomState
from nodes.filter_tech_article import filter_tech_articles
from nodes.generate_article import generate_article
from nodes.generate_prompt import generate_prompt


load_dotenv()

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "TechNews")


def determine_next_step(state: State) -> Literal["fetch_news", "filter_articles", "generate_prompts", "generate_articles", "update_dynamodb", END]:
    pass


def fetch_tech_news(state: CustomState):
    # url = "https://newsdata.io/api/1/news"
    print("###################### start #########################")
    nurl = "https://newsdata.io/api/1/latest"
    params = {"apikey": NEWS_API_KEY, "category": "technology", "language": "en"}
    response = requests.get(nurl, params=params)
    if response.status_code == 200:
        articles = response.json().get("results", [])
        fetched_articles = [{"id": str(uuid.uuid4()), **article} for article in articles]
        state.articles = fetched_articles 
        state.state_stack.append("filter_tech_articles")
        
        return {"articles": fetched_articles}
    else:
        print(f"Error fetching news: {response.status_code}")
        return {}

graph.add_node('fetch_tech_news', fetch_tech_news)
graph.add_node('filter_tech_articles', filter_tech_articles)
graph.add_node('store_news_in_dynamodb', store_news_in_dynamodb)
graph.add_node('generate_prompt', generate_prompt)
graph.add_node('generate_article', generate_article)
graph.add_node('update_article_in_dynamodb', update_article_in_dynamodb)

graph.add_edge(START, 'fetch_tech_news')
graph.add_edge('fetch_tech_news', 'filter_tech_articles')
graph.add_edge('filter_tech_articles', 'store_news_in_dynamodb')
graph.add_edge('store_news_in_dynamodb', 'generate_prompt')
graph.add_edge('generate_prompt', 'generate_article')
graph.add_edge('generate_article', 'update_article_in_dynamodb')
graph.add_edge('update_article_in_dynamodb', END)

# mem = MemorySaver()

workflow = graph.compile()


if __name__ == "__main__":
    initial_state = CustomState()
    final_state = workflow.invoke(initial_state)