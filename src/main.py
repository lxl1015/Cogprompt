from pathlib import Path
from pprint import pprint
from .config import OUTPUT_DIR, PROMPT_DIR, MAX_HOPS
from .io_utils import load_questions, load_student_proficiency
from .nlp_extractor import extract_concepts
from .kg_builder import build_ckg, _concept_node
from .graph_search import all_paths_between, one_hop_neighbors
from .prompt_generator import number_chains, to_natural_language
from .visualize import visualize_graph
from .subgraph_utils import extract_student_subgraph

import json
from .concept_names import CONCEPT_NAMES

ALL_PROMPTS_FILE = PROMPT_DIR / "all_prompts.json"


def save_prompt_json(sid, qidx, text, concepts, cogprompt_text, mastery_dict):
    mastery_lines = [
        f"- {cname}: {score:.3f}"
        for cname, score in mastery_dict.items()
    ]
    eval_prompt = (
        f"学生编号: {sid}\n"
        f"题目编号: {qidx}\n"
        f"问题: {text}\n"
        f"相关知识点: {', '.join(concepts)}\n"
        "该学生在这些知识点上的掌握度如下（0~1，数值越大表示掌握越好）:\n"
        + "\n".join(mastery_lines)
        + "\n\n"
        "稍后你将看到一条 AI 教师的回答。请基于上述学生的认知状态，评估该回答在“个性化程度/因材施教”方面的质量。"
    )

    record = {
        "student_id": sid,
        "question_index": qidx,
        "question": text,
        "concepts": concepts,          
        "mastery": mastery_dict,      
        "cogprompt": cogprompt_text,   
        "eval_prompt": eval_prompt     
    }

    if not ALL_PROMPTS_FILE.exists():
        with open(ALL_PROMPTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(ALL_PROMPTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append(record)

    with open(ALL_PROMPTS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)



def run():
    OUTPUT_DIR.mkdir(exist_ok=True)
    PROMPT_DIR.mkdir(parents=True, exist_ok=True)

    prof_df = load_student_proficiency()         
    prof_df = prof_df.set_index("student_id")

    G = build_ckg()
    visualize_graph(G, "ckg_full")

    questions = load_questions()
    for qidx, q in enumerate(questions, 1):
        sid = q["student_id"]
        text = q["question"]

        Gs = extract_student_subgraph(G, sid)
        visualize_graph(Gs, f"student{sid}_subgraph")

        concept_scores = extract_concepts(text)
        concept_nodes = [_concept_node(cid) for cid, _ in concept_scores]

        paths = all_paths_between(Gs, concept_nodes, max_len=4)
        neighbors = one_hop_neighbors(Gs, concept_nodes)

        numbered = number_chains(paths, neighbors)
        prompt_text = to_natural_language(Gs, numbered)
        for cid, cname in CONCEPT_NAMES.items():
            prompt_text = prompt_text.replace(f"c{cid}", f"({cname})")

        concept_list = []
        mastery_dict = {}
        for c, _ in concept_scores:
            if isinstance(c, str) and c.startswith("c"):
                cid = int(c[1:])
            else:
                cid = int(c)

            cname = CONCEPT_NAMES.get(cid, f"Concept {cid}")
            concept_list.append(cname)

            try:
                mastery_value = float(prof_df.loc[sid, f"c{cid}"])
            except KeyError:
                mastery_value = 0.0  
            mastery_dict[cname] = mastery_value

        outfp = PROMPT_DIR / f"student{sid}_q{qidx}.txt"
        with open(outfp, "w", encoding="utf-8") as f:
            f.write(f"Question: {text}\n")
            f.write(f"Concepts: {concept_list}\n\n")
            f.write(prompt_text)

        save_prompt_json(sid, qidx, text, concept_list, prompt_text, mastery_dict)

        print(f"[OK] Saved prompts → {outfp}")

if __name__ == "__main__":
    run()
