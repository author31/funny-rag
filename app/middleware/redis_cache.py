import os
import json
import hashlib
from app import sql_engine
from fastapi import Request
from typing import Callable, Dict
from app.redis_client import redis_client

async def cache_middleware(request: Request, call_next):
    _hashed = hashlib.md5("")
    cache_key = f"cache-{request.url.path}"
    cached_response = redis_client.get(cache_key)
    
    if cached_response is not None:
        return json.loads(cached_response)

    response = await call_next(request)
    redis_client.set(cache_key, json.dumps(response))

def db_cache_wrapper(engine: sql_engine.SQLEngine, query: str, select_data: tuple=None):
    _hash = hashlib.md5(query.encode("utf-8")).hexdigest()
    cache_key = f"cache-{_hash}"
    cached_response = redis_client.get(cache_key)
    
    if cached_response is not None: return json.loads(cached_response)

    response = engine.execute_select_query(query, select_data=select_data)
    redis_client.set(cache_key, json.dumps(response), ex=30)
    return response