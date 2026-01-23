# graph_search.py
from typing import List, Tuple
import networkx as nx
import itertools

Triple = Tuple[str, str, str]
USEFUL_RELATIONS = {"prerequisite", "similar", "master"}

def one_hop_neighbors(G, nodes):
    triples = []
    for h in nodes:
        for _, t, data in G.edges(h, data=True):
            if data["relation"] in USEFUL_RELATIONS:
                triples.append((h, data["relation"], t))
        for s, _, data in G.in_edges(h, data=True):
            if data["relation"] in USEFUL_RELATIONS:
                triples.append((s, data["relation"], h))
    return triples



def node_path_to_triples(G, node_path: List[str]) -> List[Triple]:
    triples = []
    for h, o in zip(node_path[:-1], node_path[1:]):
        found = False
        for data in G.get_edge_data(h, o).values():
            r = data.get("relation")
            if r in USEFUL_RELATIONS:
                triples.append((h, r, o))
                found = True
                break
        if not found:
            return []
    return triples


def all_paths_between(G, concepts, max_len=4):
    final_paths = []

    for a, b in itertools.combinations(concepts, 2):

        try:
            generator = nx.all_shortest_paths(G, a, b)
        except nx.NetworkXNoPath:
            continue

        try:
            shortest_paths = list(generator)
        except nx.NetworkXNoPath:
            continue

        count = 0
        for node_path in shortest_paths:
            if len(node_path) > max_len:
                continue

            triples = node_path_to_triples(G, node_path)
            if triples:
                final_paths.append(triples)
                count += 1

            if count >= 2:
                break

    return final_paths
