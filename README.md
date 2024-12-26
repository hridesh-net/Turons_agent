# 📰 Turons Agent
Latest News Filter and Notifier

Welcome to the Latest News Filter and Notifier! 🚀
Keep yourself updated with the latest news in the easiest way possible. Whether you’re into tech, fashion, sports, or any other topic, this project lets you stay informed with customized news updates and concise content summaries.

----

### 🌟 Features

#### 1.	Personalized News Updates:

Default category is Technology, but you can change it to any topic you like (e.g., health, business, entertainment).

#### 2.	AI-Powered Filtering

Not all “tech” news is actually about tech. Our built-in AI filters ensure you get relevant, high-quality articles.

#### 3.	Half-Minute Reads

Don’t have time to read long articles? The project summarizes news into easy-to-read, concise content so you can stay informed in just 30 seconds.

#### 4.	Seamless Integration with DynamoDB

All filtered news articles are stored in AWS DynamoDB with their content and status for easy management and tracking.

#### 5.	Notifications for Latest Articles

The project keeps you up-to-date by notifying you whenever new, relevant articles are available.
#### 6.	Two Modes to Run

- main.py: For a straightforward execution.

- lg_app.py: The LangGraph-powered version, offering a modular, state-based workflow for advanced use cases.
-----

### 🏗️ Project Structure

Here’s a breakdown of the project directory:
```bash
.
├── main.py                 # The simple version of the application
├── lg_app.py               # The LangGraph-powered version
├── nodes/                  # State nodes for LangGraph
│   ├── db_node.py          
│   ├── filter_tech_article.py 
│   ├── generate_article.py 
│   ├── generate_prompt.py  
│   ├── state_manager.py    
├── utils/                  # Utility functions and classes
│   ├── aws_utils.py        
│   ├── base_utils_class.py 
│   ├── data_utils.py       
└── README.md
```
----


### 🚀 How It Works

#### 1️⃣ Fetch News

Using the NewsData API, the project fetches the latest news articles from the selected category (default: technology).

#### 2️⃣ AI-Powered Filtering

Articles are passed to an AI agent to identify the most relevant ones for your chosen category.

#### 3️⃣ Content Summarization

Filtered articles are summarized into concise, engaging pieces that you can read in half a minute. AI ensures summaries are simple, understandable, and free of clutter.

#### 4️⃣ Store and Notify

Filtered articles are stored in AWS DynamoDB with their summaries and status. Notifications ensure you’re always updated.

----

### 🛠️ How to Use

#### Prerequisites
- Python 3.12+
- AWS account with DynamoDB configured
- NewsData API key
- Groq API key

#### Installation
1.	Clone this repository:
```bash
git clone https://github.com/your-repo/latest-news-filter.git
cd latest-news-filter
```

2.	Install dependencies:
```bash
pip install -r requirements.txt
```

3.	Configure environment variables:
Create a .env file with the following variables:

```bash
NEWS_API_KEY=your_newsdata_api_key
GROQ_API_KEY=your_groq_api_key
AWS_REGION=your_aws_region
AWS_ACCESS_KEY=your_aws_access_key
AWS_SECRET_KEY=your_aws_secret_key
DYNAMODB_TABLE=TechNews
```


#### Running the Application

1. Simple Mode
```bash
python main.py
```
2. LangGraph Mode
```bash
python lg_app.py
```
----

### ✨ Why Choose This Project?
1.	Scalable and Modular

Whether you’re a beginner or an advanced user, this project is easy to use and extend.

2.	Stay Updated

Get personalized, summarized news updates every day without spending hours scrolling.

3.	AI-Powered Precision

Leverages cutting-edge AI for content filtering and summarization.

4.	Customizable

Easily switch categories to focus on what matters to you.

----

### 🤝 Contributing

We love contributions! If you have ideas to improve this project or want to fix something, feel free to fork the repo and create a pull request.

---

### 🛡️ Disclaimer

This project uses external APIs and services. Ensure you comply with their terms of use.

Enjoy staying informed effortlessly with Latest News Filter and Notifier! 🎉