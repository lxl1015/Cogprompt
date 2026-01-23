import networkx as nx

def extract_student_subgraph(G: nx.MultiDiGraph, student_id: int) -> nx.MultiDiGraph:
    sid = f"s{student_id}"
    if sid not in G:
        raise ValueError(f"Student node {sid} not found in graph.")

    neighbors_1 = set(G.successors(sid))
    neighbors_2 = set()
    for n in neighbors_1:
        neighbors_2.update(G.successors(n))

    nodes_to_keep = {sid} | neighbors_1 | neighbors_2

    subG = G.subgraph(nodes_to_keep).copy()
    subG.graph["student_id"] = student_id
    return subG
