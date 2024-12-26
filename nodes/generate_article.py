from nodes.state_manager import CustomState, graph
from utils.base_utils_class import ArticleAgent


def generate_article(state: CustomState):
    print("###################### Article Gen #########################")
    if len(state.filtered_articles) > 0:
        res_dict = dict()
        for article in state.filtered_articles:
            print(f"doing for article ID: {article.get("id")}")
            try:
                id = article.get("id")
                prompt_text = state.prompt.get(id)
                content = state.raw_content.get(id)
                if prompt_text and content:
                    article = ArticleAgent(prompt_text, content)
                    news_article = article.generate_article()
                    res_dict[article.get("id")] = news_article
                    state.article_content[article.get("id")] = news_article
            except Exception as e:
                print(f"Error in article generation: {e}")
                continue
        
        state.state_stack.append("update_article_in_dynamodb")
        return {"article_content": res_dict}
    
    state.state_stack.pop()
    return {}