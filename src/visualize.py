from pathlib import Path
from pyvis.network import Network
import networkx as nx
from .config import GRAPH_DIR

def visualize_graph(G:nx.MultiDiGraph, name:str):
    GRAPH_DIR.mkdir(parents=True, exist_ok=True)
    net = Network(height="700px", width="100%", directed=True, notebook=False)
    net.toggle_physics(True)

    color = {"student":"#4C78A8","exercise":"#F58518","concept":"#72B7B2"}
    for n, data in G.nodes(data=True):
        t = data.get("type","literal")
        net.add_node(n, label=n, color=color.get(t, "#B0B0B0"), title=str(data))

    for u, v, k, d in G.edges(keys=True, data=True):
        rel = d.get("relation","")
        net.add_edge(u, v, label=rel)

    out = GRAPH_DIR / f"{name}.html"
    net.write_html(str(out))
    return out
