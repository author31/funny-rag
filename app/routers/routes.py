from fastapi import APIRouter, HTTPException
from app.redis_client import redis_client
from app.engine.builder import TrieBuilder
from config.settings import HN_URL

router = APIRouter()

@router.get("/suggestion/")
def get_suggestion(prefix: str):
    result = redis_client.lrange(prefix, 0, -1)
    if len(result) > 0: return result
    trie_builder = TrieBuilder(url=HN_URL, redis_client=redis_client)
    correspond_node = trie_builder.trie_tree.search(word= prefix)
    freq_list = trie_builder.trie_tree.get_node_topk(correspond_node)
    return [f["word"] for f in freq_list]