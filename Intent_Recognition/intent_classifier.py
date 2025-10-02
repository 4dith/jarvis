# !pip install sentence-transformers spacy
# !python -m spacy download en_core_web_sm

from sentence_transformers import SentenceTransformer, util
import spacy

# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # small & fast

intent_embeddings = {}
for intent, examples in intents.items():
    intent_embeddings[intent] = model.encode(examples, convert_to_tensor=True)

# 4. Function: classify intent
def classify_intent(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    best_intent = None
    best_score = -1

    for intent, examples_emb in intent_embeddings.items():
        # cosine similarity between input and each intent's examples
        similarity = util.cos_sim(user_embedding, examples_emb).max().item()
        if similarity > best_score:
            best_score = similarity
            best_intent = intent

    return best_intent, best_score