import networkx as nx

def multi_hop_expand(G, start_node, max_depth=3, visited=None):
    if visited is None:
        visited = set()
    visited.add(start_node)

    neighbors = set(G.successors(start_node))
    expanded = set(neighbors)

    if max_depth > 1:
        for n in neighbors:
            if n not in visited:
                deeper = multi_hop_expand(G, n, max_depth=max_depth-1, visited=visited)
                expanded |= deeper
    return expanded


def all_paths_between(G, concept_nodes, expand_depth=10, max_path_len=10):
    all_paths = []

    for source in concept_nodes:
        reachable = multi_hop_expand(G, source, max_depth=expand_depth)
        for target in concept_nodes:
            if target in reachable and source != target:
                try:
                    for path in nx.all_simple_paths(G, source=source, target=target, cutoff=max_path_len):
                        if len(path) >= 3:
                            all_paths.append(path)
                except nx.NetworkXNoPath:
                    continue
    return all_paths
