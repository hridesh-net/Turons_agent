import os
import uuid
import boto3
import requests
from dotenv import load_dotenv

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


def store_news_in_dynamodb(filtered_articles):
    for news in filtered_articles:
        try:
            news["posted"] = False
            table.put_item(Item=news)
            print(f"Stored in DynamoDB: {news['title']}")
        except Exception as e:
            print(f"Error storing news in DynamoDB: {e}")


def update_article_in_dynamodb(news_id, article_content):
    try:
        table.update_item(
            Key={"id": news_id},
            UpdateExpression="SET Article = :article",
            ExpressionAttributeValues={":article": article_content},
        )
        print(f"Updated NewsID {news_id} with article content.")
    except Exception as e:
        print(f"Failed to update DynamoDB: {str(e)}")