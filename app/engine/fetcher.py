import requests
from typing import List, Dict
from .connection import insert_posts, get_posts

BASE_URL = "{url}/item/{post_idx}.json"

def fetch_api(url: str, post_idx: int) -> Dict:
    return requests.get(BASE_URL.format(url=url, post_idx=post_idx)).json()

# what if using async/await ??
def fetch_top_stories_ids(url: str, topk: int = 300) -> None:
    response = requests.get(f"{url}/topstories.json")
    post_ids = response.json()[:topk]
    return post_ids

def fetch_top_stories(url: str, topk: int= 300) -> List[Dict]:
    existed_posts = get_posts()
    if len(existed_posts) > 0: return
    post_ids = fetch_top_stories_ids(url, topk)
    results = [(fetch_api(url, post_idx)["title"], BASE_URL.format(url=url, post_idx=post_idx))
               for post_idx in post_ids]
        
    if len(results > 0): insert_posts(results)
