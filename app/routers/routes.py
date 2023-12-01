import os
from config.settings import HN_URL

from app.models import ClusterModel
from app.redis_client import redis_client
from app import sql_engine, together_client
from app.engine.builder import TrieBuilder
from app.middleware.redis_cache import db_cache_wrapper

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

template = Jinja2Templates(directory="views")
    
engine = sql_engine.SQLEngine(
    host= os.getenv("POSTGRESQL_URL"),
    database= "postgres",
    user= "postgres",
    password= os.getenv("POSTGRESQL_PWD"),
    minconn= 1,
    maxconn= 5
)

@router.get("/", response_class=HTMLResponse)
def get_homepage(request: Request):
    query = \
    """
    SELECT * FROM hn_cluster_titles
    ORDER BY hn_cluster_idx ASC
    """
    
    results = db_cache_wrapper(engine=engine, query=query)
    cluster_data = {r[0]:r[1] for r in results}
    return template.TemplateResponse("homepage.html", {"request": request, "cluster_data": cluster_data})

@router.get("/answer", response_class=HTMLResponse)
def get_homepage(request: Request, answer: str):
    return template.TemplateResponse("answer.html", {"request": request, "answer": answer})

@router.get("/suggestion/")
def get_suggestion(prefix: str):
    result = redis_client.lrange(prefix, 0, -1)
    if len(result) > 0: return result
    trie_builder = TrieBuilder()
    correspond_node = trie_builder.trie_tree.search(word= prefix)
    if isinstance(correspond_node, str) and correspond_node == "wordNotFound": return []
    freq_list = trie_builder.trie_tree.get_node_topk(correspond_node)
    return [f["word"] for f in freq_list]

@router.post("/retrieve")
def retrieve_answer(cluster_data: ClusterModel):
    client = together_client.TogetherClient()
    # results = client.get_records_by_cluster_idx(cluster_idx=cluster_data.hn_cluster_idx)
    # titles = [r["title"] for r in results]
    # return client.retrieve_answer(question=cluster_data.question, titles=titles)
    return "hi"