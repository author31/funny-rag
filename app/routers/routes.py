import os
from config.settings import HN_URL
from app.redis_client import redis_client
from app.engine.builder import TrieBuilder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.middleware.redis_cache import db_cache_wrapper
from fastapi import APIRouter, HTTPException, Request

router = APIRouter()

template = Jinja2Templates(directory="views")

@router.get("/", response_class=HTMLResponse)
def get_homepage(request: Request):
    query = \
    """
    SELECT * FROM hn_cluster_titles
    ORDER BY hn_cluster_idx ASC
    """
    
    results = db_cache_wrapper(query)
    cluster_data = {r[0]:r[1] for r in results}
    return template.TemplateResponse("homepage.html", {"request": request, "cluster_data": cluster_data})

@router.get("/suggestion/")
def get_suggestion(prefix: str):
    result = redis_client.lrange(prefix, 0, -1)
    if len(result) > 0: return result
    trie_builder = TrieBuilder()
    correspond_node = trie_builder.trie_tree.search(word= prefix)
    if isinstance(correspond_node, str) and correspond_node == "wordNotFound": return []
    freq_list = trie_builder.trie_tree.get_node_topk(correspond_node)
    return [f["word"] for f in freq_list]