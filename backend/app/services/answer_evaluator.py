import re

def normalise_answer(answer: str) -> str:
    answer = answer.lower().strip()
    answer = re.sub(r"[^\w\s]", "", answer)
    answer = re.sub(r"\s+", " ", answer)
    return answer
def evaluate_answer(user_answer: str, expected_answer: str) -> bool:
    return normalise_answer(user_answer) == normalise_answer(expected_answer)