from .builder import TrieBuilder
from config.settings import HN_URL
from redis_client import redis_client
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    trie_builder = TrieBuilder(url=HN_URL, redis_client=redis_client)
    trie_builder.init_builder()
    yield
