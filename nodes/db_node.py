import os
import uuid
import boto3
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

from nodes.state_manager import CustomState, graph
from langgraph.graph import END

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "TechNews")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")


##########################################
# Initalizing DynamoDB
##########################################

dynamodb = dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)
table = dynamodb.Table(DYNAMODB_TABLE)



def store_news_in_dynamodb(state: CustomState):
    print("###################### Db storing #########################")
    if state.filtered_articles:
        for news in state.filtered_articles:
            try:
                news["posted"] = False
                table.put_item(Item=news)
                print(f"Stored in DynamoDB: {news['title']}")
            except Exception as e:
                print(f"Error storing news in DynamoDB: {e}")
        state.state_stack.append("generate_prompt")
        return {"db_stored": True}
    else:
        state.state_stack.pop()
        return {"db_stored": False}



def update_article_in_dynamodb(state: CustomState):
    print("###################### Db Updating #########################")
    print(state.article_content)
    for id, news_content in state.article_content:
        print(f"Updating artcile id: {id}")
        try:
            table.update_item(
                Key={"id": id},
                UpdateExpression="SET Article = :article",
                ExpressionAttributeValues={":article": news_content},
            )
            print(f"Updated NewsID {id} with article content.")
        except Exception as e:
            print(f"Failed to update DynamoDB: {str(e)}")
            continue
    
    state.state_stack.append("END")
    return {"db_update": True}