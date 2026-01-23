from typing import List, Tuple, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .knowledge_base import KNOWLEDGE_KEYWORDS
from .config import BERT_MODEL_NAME, TOPK_CONCEPTS_PER_QUESTION

def _flatten_kws() -> Dict[int, str]:
    return {cid: " ".join(kws) for cid, kws in KNOWLEDGE_KEYWORDS.items()}

def _bert_encode(texts: List[str]):
    try:
        from transformers import AutoTokenizer, AutoModel
        import torch
        tok = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)
        model = AutoModel.from_pretrained(BERT_MODEL_NAME)
        model.eval()
        with torch.no_grad():
            outs = []
            for t in texts:
                enc = tok(t, return_tensors="pt", truncation=True, padding=True)
                emb = model(**enc).last_hidden_state.mean(dim=1)  # [1,d]
                outs.append(emb.squeeze(0).cpu().numpy())
        return np.vstack(outs)
    except Exception:
        return None 

def _tfidf_encode(texts: List[str]):
    vec = TfidfVectorizer()
    X = vec.fit_transform(texts)
    return X, vec

def extract_concepts(question: str, topk: int = TOPK_CONCEPTS_PER_QUESTION) -> List[Tuple[int, float]]:
    kb = _flatten_kws()
    texts = [question] + [kb[cid] for cid in sorted(kb)]
    bert = _bert_encode(texts)
    if bert is not None:
        qv = bert[0:1]
        kv = bert[1:]
        sims = cosine_similarity(qv, kv).ravel()
        pairs = list(zip(sorted(kb), sims))
        pairs.sort(key=lambda x: x[1], reverse=True)
        return pairs[:topk]

    X, _ = _tfidf_encode(texts)
    sims = cosine_similarity(X[0:1], X[1:]).ravel()
    pairs = list(zip(sorted(kb), sims))
    pairs.sort(key=lambda x: x[1], reverse=True)
    return pairs[:topk]
