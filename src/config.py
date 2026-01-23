from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
GRAPH_DIR = OUTPUT_DIR / "graphs"
PROMPT_DIR = OUTPUT_DIR / "prompts"

NUM_CONCEPTS = 9

SIMILAR_THRESHOLD = 0.32

MAX_HOPS = 3
MAX_PATHS_PER_PAIR = 12

BERT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TOPK_CONCEPTS_PER_QUESTION = 3
