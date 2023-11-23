import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
HN_URL = "https://hacker-news.firebaseio.com/v0"