import re

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Load the model when backend starts
model = SentenceTransformer("all-MiniLM-L6-v2")

def normalise_answer(answer: str) -> str:
    answer = answer.lower().strip()
    answer = re.sub(r"[^\w\s]", "", answer)
    answer = re.sub(r"\s+", " ", answer)
    return answer
def evaluate_answer(user_answer: str, expected_answer: str, similarity_threshold: float = 0.75) -> dict:
    normalise_user = normalise_answer(user_answer)
    normalise_expected = normalise_answer(expected_answer)

    # Exact match
    if normalise_user == normalise_expected:
        return{
            "correct": True,
            "similarity_score": 1.0,
            "evaluation_method": "exact_match",
        }
    # create sentence embeddings
    embeddings = model.encode(
        [normalise_user, normalise_expected],
        convert_to_tensor=True
    )
    # calculate cosine similarity
    similarity = cos_sim(
        embeddings[0],
        embeddings[1]
    ).item()
    return {
        "correct": similarity >= similarity_threshold,
        "similarity_score": similarity,
        "evaluation_method": "semantic_similarity",
    }