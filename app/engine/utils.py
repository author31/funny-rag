from typing import Iterator, List, Callable
from copy import deepcopy
from functools import reduce

def ilen(iterator: Iterator):
    cloned = deepcopy(iterator)
    return reduce(lambda x, _: x+1, cloned, 0)

def pprint(node):
    if not node: return
    children = filter(lambda x: x, node.children)
    if ilen(children) == 0: return
    print(f"Node: {node.char}")
    print(f"--- Children: {list(children)}")
    for n in node.children: pprint(n)

def flatten_ls(items: List, func: Callable = lambda x: x) -> List:
    return [func(j) for i in items for j in i]