from typing import List, Dict, Tuple
import networkx as nx
from .prompt_templates import triple_to_sentence

def number_chains(paths:List[List[Tuple[str,str,str]]], neighbors:List[Tuple[str,str,str]]):
    numbered = {"paths": [], "neighbors": []}
    for idx, chain in enumerate(paths, 1):
        numbered["paths"].append((f"P{idx}", chain))
    for idx, triple in enumerate(neighbors, 1):
        numbered["neighbors"].append((f"N{idx}", [triple]))
    return numbered

def triples_with_attrs(G:nx.MultiDiGraph, triples):
    out = []
    for h, r, o in triples:
        data = None
        if G.has_edge(h, o):
            for k, d in G.get_edge_data(h, o).items():
                if d.get("relation") == r:
                    data = d; break
        out.append((h, r, o, data or {}))
    return out

def to_natural_language(G:nx.MultiDiGraph, numbered):
    lines = []
    # Paths
    for pid, chain in numbered["paths"]:
        lines.append(f"[{pid}]")
        for h, r, o in chain:
            _, _, _, attrs = next(iter(triples_with_attrs(G, [(h,r,o)])))
            lines.append(" - " + triple_to_sentence(h, r, o, attrs))
    # Neighbors
    for nid, chain in numbered["neighbors"]:
        lines.append(f"[{nid}]")
        for h, r, o in chain:
            _, _, _, attrs = next(iter(triples_with_attrs(G, [(h,r,o)])))
            lines.append(" - " + triple_to_sentence(h, r, o, attrs))
    return "\n".join(lines)
