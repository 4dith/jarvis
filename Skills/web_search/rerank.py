from sentence_transformers import SentenceTransformer, util # type: ignore

_model = None
def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def rerank_snippets(query, snippets, top_k=5):
    """
    snippets: list of dicts with keys 'text' and optional 'link'
    returns reordered list by similarity to query
    """
    model = _get_model()
    q_emb = model.encode(query, convert_to_tensor=True)
    texts = [s["text"] for s in snippets]
    emb = model.encode(texts, convert_to_tensor=True)
    scores = util.cos_sim(q_emb, emb)[0]
    idxs = scores.argsort(descending=True).cpu().numpy().tolist()
    return [snippets[i] for i in idxs[:top_k]]