import os
import re
from trie.trie import Trie
from app import sql_engine
from typing import List, Any
from dotenv import load_dotenv
from .utils import flatten_ls
from app.engine.fetcher import fetch_top_stories

load_dotenv()

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
        self.trie_tree = Trie()
        self.sql_engine = sql_engine.SQLEngine(
            host= os.getenv("POSTGRESQL_URL"),
            database= "postgres",
            user= "postgres",
            password= os.getenv("POSTGRESQL_PWD"),
            minconn= 1,
            maxconn= 5
        )
    
    def clean_symbols(self, word: str) -> str:
        return re.sub(r'[^a-z]', "", word.lower())

    def init_builder(self) -> None:
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
            if not node: continue
            for topk in node.cache_topk:
                self.redis_client.rpush(node.char, topk["word"])

    def _santitize_word(self, word: str) -> str:
        word = word.replace("-", " ")
        word = re.sub(r"[^a-z\s]", "", word.lower())
        word = re.sub(r"\s+", " ", word)
        return word
        
    def _build_trie(self) -> None:
        titles = self._get_cluster_titles()
        titles = [self._santitize_word(t) for t in titles]
        self.trie_tree.build_sentence_trie(vocabs=titles)
        self.trie_tree.init_cache()
        
    def _fetch_data(self):
        fetch_top_stories(url=self.url, topk=300)
        
    def _tuple_to_dict(self, tuple_data, keys=None) -> dict:
        return dict(zip(keys, tuple_data))

    def _get_cluster_titles(self, limit: int=10) -> List[str]:
        query = \
        """
        SELECT * FROM hn_cluster_titles
        LIMIt %s
        """
        results = self.sql_engine.execute_select_query(query, (limit,))
        keys = ["hn_cluster_idx", "title"]
        return [self._tuple_to_dict(result, keys)["title"] for result in results]