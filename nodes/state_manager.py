from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

class CustomState(BaseModel):
    articles: list[dict] = Field(default_factory=list)
    filtered_articles: list[dict] = Field(default_factory=list)
    raw_content: dict = Field(default_factory=dict)
    article_content: dict = Field(default_factory=dict)
    prompt: dict = Field(default_factory=dict)
    state_stack: list = Field(default_factory=list)
    db_stored: bool = Field(default=False)
    db_update: bool = Field(default=False)

class State:
    def __init__(self, raw_data: list = [], node = "fetch_tech_news", filtered_data: list = None, news_id = None, title = None, link = None):
        self.articles = raw_data
        self.filtered_articles = filtered_data
        self.id = news_id
        self.title = title
        self.url = link
        self.raw_content: dict = {}
        self.article_content: dict = {}
        self.prompt: dict = {}
        self.state_stack = []
        self.state_stack.append(node)

graph = StateGraph(CustomState)