from .builder import TrieBuilder
from config.settings import HN_URL
from app.redis_client import redis_client
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    trie_builder = TrieBuilder()
    trie_builder.init_builder()
    yield