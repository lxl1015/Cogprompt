import itertools
import networkx as nx
import numpy as np
import pandas as pd
from collections import defaultdict
from .config import NUM_CONCEPTS
from .knowledge_base import PREREQUISITES, SIMILAR
from .io_utils import load_student_proficiency, load_exercise_params, load_responses
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .knowledge_base import KNOWLEDGE_KEYWORDS 
from .concept_names import CONCEPT_NAMES



def _concept_node(cid:int) -> str: return f"c{cid}"
def _student_node(sid:int) -> str: return f"s{sid}"
def _exercise_node(eid:int) -> str: return f"e{eid}"

def aggregate_concept_difficulty(ex_params: pd.DataFrame) -> dict:
    diffs = {f"c{i}": ex_params[f"c{i}"].mean() for i in range(1, NUM_CONCEPTS+1)}
    return diffs

def build_ckg():
    G = nx.MultiDiGraph(name="CKG")

    prof = load_student_proficiency()
    ex_params = load_exercise_params()
    responses = load_responses()

    for sid in prof["student_id"].tolist():
        G.add_node(_student_node(sid), type="student")

    for _, row in ex_params.iterrows():
        G.add_node(_exercise_node(int(row["exercise_id"])), type="exercise",
                   discrimination=float(row["discrimination"]))

    for cid in range(1, NUM_CONCEPTS+1):
        cname = CONCEPT_NAMES.get(cid, f"Concept {cid}")
        G.add_node(_concept_node(cid), type="concept", name=cname)

    for _, row in prof.iterrows():
        sid = int(row["student_id"])
        for cid in range(1, NUM_CONCEPTS+1):
            master = float(row[f"c{cid}"])
            G.add_edge(_student_node(sid), _concept_node(cid),
                       key=f"master_{sid}_{cid}", relation="master", weight=master, master=master)

    by_exercise = defaultdict(set)
    for rec in responses:
        eid = int(rec["problem_id"])
        sid = int(rec["user_id"])
        score = float(rec["score"])
        kcodes = rec.get("knowledge_code", []) or []
        G.add_edge(_student_node(sid), _exercise_node(eid),
                   key=f"score_{sid}_{eid}", relation="score", score=score)
        for k in kcodes:
            if k == 0: 
                continue
            G.add_edge(_exercise_node(eid), _concept_node(k),
                       key=f"include_{eid}_{k}", relation="include")
            by_exercise[eid].add(k)

    c_difficulty = aggregate_concept_difficulty(ex_params)
    for cnode, diff in c_difficulty.items():
        G.add_edge(cnode, f"diff:{diff:.3f}", relation="difficulty")

    for _, row in ex_params.iterrows():
        eid = int(row["exercise_id"])
        disc = float(row["discrimination"])
        G.add_edge(_exercise_node(eid), f"disc:{disc:.3f}", relation="discrimination")

    for a, b in PREREQUISITES:
        G.add_edge(_concept_node(a), _concept_node(b), relation="prerequisite")

    for a, b in SIMILAR:
        G.add_edge(_concept_node(a), _concept_node(b), relation="similar")
        G.add_edge(_concept_node(b), _concept_node(a), relation="similar")

    return G

