import re
from .trie import Trie
from typing import List, Any
from .utils import flatten_ls
from app.engine.connection import init_db, get_posts
from app.engine.fetcher import fetch_top_stories

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls in cls._instances: return cls._instances[cls]
        instance = super().__call__(*args, **kwargs)
        cls._instances[cls] = instance
        return cls._instances[cls]

class TrieBuilder(metaclass=Singleton):
    def __init__(self, url: str, redis_client: Any = None) -> None:
        self.url = url
        self.redis_client = redis_client
        self.trie_tree = Trie(topk=10)
    
    def clean_symbols(self, word: str) -> str:
        return re.sub(r'[^a-z]', "", word.lower())

    def init_builder(self) -> None:
        init_db()
        self._fetch_data()
        self._build_trie()
        self._set_cache()
        
        
    def _set_cache(self) -> None:
        if not self.redis_client: return
        is_set_cache = len(self.redis_client.keys())==0

        if not is_set_cache: 
            print("skipping caching setting")
            return

        for node in self.trie_tree.root_node.children:
            for topk in node.cache_topk:
                self.redis_client.rpush(node.char, topk["word"])

    def _build_vocabs(self) -> List:
        posts = get_posts()
        vocabs = [word.split(" ") 
                  for post in posts 
                  for word in post]
        
        return flatten_ls(items=vocabs, func=self.clean_symbols)
    
    def _build_trie(self) -> None:
        vocabs = self._build_vocabs()
        self.trie_tree.build_trie(vocabs)
        self.trie_tree.init_cache()
        
    def _fetch_data(self):
        fetch_top_stories(url=self.url, topk=300)