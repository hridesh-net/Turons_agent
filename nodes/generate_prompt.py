from nodes.state_manager import CustomState, graph
from utils.base_utils_class import PromptAgent


def generate_prompt(state: CustomState):
    print("###################### Prompt Gen #########################")
    res_prompt = dict()
    for article in state.filtered_articles:
        try:
            prompt = PromptAgent(article, article.get("id"))
            prompt_text = prompt.generate_prompt()
            content = prompt.get_content()
            res_prompt[article.get("id")] = prompt_text
            state.prompt[article.get("id")] = prompt_text
            state.raw_content[article.get("id")] = content
        except Exception as e:
            print(f"Got Error {e} in article id: {article.get("id")}")
            state.filtered_articles.remove(article)
            continue
    if len(state.filtered_articles) > 0:
        state.state_stack.append("generate_article")
        return {"prompt": res_prompt}
    state.state_stack.pop()
    return {}