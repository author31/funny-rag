from utils import ilen
from typing import List, Dict

class TrieNode:
    def __init__(self, char: str = "") -> None:
        self.char: str = char
        self.freq: int = 0
        self.is_end_of_word: bool = False
        self.children: List = [None for _ in range(26)]
        self.cache_topk: List[Dict] = []
        
    def has_children(self) -> bool:
        filtered_children = filter(lambda x: x, self.children)
        return ilen(filtered_children) > 0
    
    def __repr__(self) -> str:
        return f"Node: {self.char}, Freq: {self.freq}"

class Trie:
    def __init__(self, topk: int = 3) -> None:
        self.root_node = TrieNode()
        self.topk: int = topk
        
    def char_to_idx(self, char: str) -> int:
        return ord(char) - ord("a")

    def build_trie(self, vocabs: List) -> None:
        for word in vocabs: self.insert_trie(word)

    def insert_trie(self, word):
        temp_node = self.root_node
        for idx in range(len(word)):
            char_idx = self.char_to_idx(word[idx])

            if not temp_node.children[char_idx]: 
                temp_node.children[char_idx] = TrieNode(word[:idx+1])

            if word == temp_node.children[char_idx].char and idx == len(word)-1: 
                temp_node.children[char_idx].freq += 1

            if idx == len(word)-1:
                temp_node.children[char_idx].is_end_of_word = True

            temp_node = temp_node.children[char_idx]
            
    def init_cache(self):
        if not self.root_node.has_children(): raise Exception("Trie is empty")
        for node in self.root_node.children: 
            if not node: continue
            self._cache_topk(node)

    def get_topk(self, topk: int = None) -> List[Dict]:
        if not topk: topk = self.topk
        freq_list = []
        self._get_freq(self.root_node, freq_list)
        return sorted(freq_list, key=lambda x: x["freq"], reverse=True)[:topk]

    def get_node_topk(self, node: TrieNode, topk: int = None) -> List[Dict]:
        if not topk: topk = self.topk
        freq_list = []
        self._get_freq(node, freq_list)
        return sorted(freq_list, key=lambda x: x["freq"], reverse=True)[:topk]

    def _get_freq(self, node: TrieNode, freq_list: List) -> None:
        if not node: return
        if node.is_end_of_word: freq_list.append({"word": node.char, "freq": node.freq})
        for n in node.children: self._get_freq(n, freq_list)

    def _cache_topk(self, node: TrieNode) -> None:
        freq_list = self.get_node_topk(node)
        for f in freq_list:
            word_idx = self.char_to_idx(f["word"][0])
            node = self.root_node.children[word_idx]
            node.cache_topk.append(f)