from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.redis_client import redis_client
from app.engine.builder import TrieBuilder
from config.settings import HN_URL

router = APIRouter()

template = Jinja2Templates(directory="views")

@router.get("/", response_class=HTMLResponse)
def get_homepage(request: Request):
    return template.TemplateResponse("homepage.html", {"request": request})

@router.get("/suggestion/")
def get_suggestion(prefix: str):
    result = redis_client.lrange(prefix, 0, -1)
    if len(result) > 0: return result
    trie_builder = TrieBuilder(url=HN_URL, redis_client=redis_client)
    correspond_node = trie_builder.trie_tree.search(word= prefix)
    if isinstance(correspond_node, str) and correspond_node == "wordNotFound": return []
    freq_list = trie_builder.trie_tree.get_node_topk(correspond_node)
    return [f["word"] for f in freq_list]