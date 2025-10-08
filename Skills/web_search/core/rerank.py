# rerank.py
from sentence_transformers import SentenceTransformer, util
import torch
from config import RERANK_MODEL

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(RERANK_MODEL)
    return _model

def rerank_snippets(query, snippets, top_k=5):
    """Rerank search snippets by semantic similarity to query."""
    if not snippets:
        return []

    model = _get_model()
    q_emb = model.encode(query, convert_to_tensor=True)
    emb = model.encode([s["text"] for s in snippets], convert_to_tensor=True)
    scores = util.cos_sim(q_emb, emb)[0]
    idxs = torch.argsort(scores, descending=True).tolist()
    return [snippets[i] for i in idxs[:top_k]]
