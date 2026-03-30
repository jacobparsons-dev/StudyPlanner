import math

def compute_recall_prob(days_since_review, successful_reviews, avg_confidence, difficulty):
    base_stability = 2.0
    stability = (
        base_stability
        + successful_reviews * 1.5
        + avg_confidence * 0.4
        - difficulty * 0.3
    )
    stability = max(stability, 0.5)
    recall_prob = math.exp(-days_since_review / stability)
    return max(0.0, min(1.0, recall_prob))