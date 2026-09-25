import math

def compute_recall_prob(days_since_review, successful_reviews, failed_reviews, avg_confidence, difficulty):
    base_stability = 1.0

    # sucessful improve stability, diminishing returns though
    review_bonus = math.log1p(successful_reviews) * 2.0

    # failed reduce stability
    failure_penalty = failed_reviews * 1.5

    # higher confidence improve
    confidence_bonus = avg_confidence * 0.5

    # higher diff makes recall delay quickekr
    difficulty_penalty = difficulty * 0.5

    stability = base_stability + review_bonus + confidence_bonus - failure_penalty - difficulty_penalty
    # stability can't be 0 or negative
    stability = max(stability, 0.1)

    # exponential forgetting curve
    recall_probability = math.exp(-days_since_review / stability)

    return max(0.0, min(1.0, recall_probability))