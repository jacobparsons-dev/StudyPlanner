import numpy as np
import pandas as pd
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import(
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import GroupShuffleSplit
data = pd.read_csv("ml/answer_training_data_v2.csv")

print(f"Loaded {len(data)} training examples")
print(f"Questions: {data['question_id'].nunique()}")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_features(questions,expected_answers,student_answers):
    """
    Turn each expected/student answer pair into numerical features
    that classifier can learn from
    """
    question_embeddings = embedding_model.encode(
        questions.tolist(),
        convert_to_numpy=True,
    )
    expected_embeddings = embedding_model.encode(
        expected_answers.tolist(),
        convert_to_numpy= True,
    )
    student_embeddings = embedding_model.encode(
        student_answers.tolist(),
        convert_to_numpy=True,
    )
    # How different
    answer_difference = np.abs(
        expected_embeddings - student_embeddings
    )
    # Where do they agree
    answer_interaction = (
        expected_embeddings * student_embeddings
    )
    question_difference = np.abs(
        question_embeddings - student_embeddings
    )
    question_interaction = (
        question_embeddings * student_embeddings
    )
    # combine feature sets
    return np.concatenate(
        [
            answer_difference,
            answer_interaction,
            question_difference,
            question_interaction,
        ],
        axis=1
    )
X = create_features(
    data['question'],
    data["expected_answer"],
    data["student_answer"],
)
y = data["label"].values

print(f"Feature matrix shape: {X.shape}")

# Split examples into training and test data
groups = data["question_id"].values
splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.2,
    random_state=42,
)
train_indices, test_indices = next(
    splitter.split(X,y,groups)
)
X_train = X[train_indices]
X_test = X[test_indices]
y_train = y[train_indices]
y_test = y[test_indices]

train_questions = set(
    data.iloc[train_indices]["question_id"]
)
test_questions = set(
    data.iloc[test_indices]["question_id"]
)

print("\nDataset split")

print(f"Training examples: {len(X_train)}")
print(f"Testing examples:  {len(X_test)}")
print(f"Training questions: {len(train_questions)}")
print(f"Testing questions:  {len(test_questions)}")

print(
    f"Question overlap: "
    f"{len(train_questions.intersection(test_questions))}"
)

classifier = LogisticRegression(
    max_iter=2000,
)
classifier.fit(X_train, y_train)

# test on answers the classifier wasn't trained on
predictions = classifier.predict(X_test)


print("\nModel evaluation")
print(f"Accuracy:  {accuracy_score(y_test, predictions):.3f}")

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "incorrect",
            "partial",
            "correct",
        ],
        digits=3,
    )
)

print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions))

# Show mistakes
test_data = data.iloc[test_indices].copy()
test_data["prediction"] = predictions
mistakes = test_data[
    test_data["label"] != test_data["prediction"]
]
print("\nMisclassified examples")
for _, row in mistakes.head(10).iterrows():
    print(f"\nQuestion: {row['question']}")
    print(
        f"Expected answer: "
        f"{row['expected_answer']}"
    )
    print(
        f"Student answer: "
        f"{row['student_answer']}"
    )
    print(
        f"Actual: {row['label_name']}"
    )
    predicted_name = {
        0: "incorrect",
        1: "partial",
        2: "correct",
    }[row["prediction"]]
    print(
        f"Predicted: {predicted_name}"
    )

# save the trained classifier
joblib.dump(
    classifier,
    "ml/answer_classifier_v2.joblib"
)
print("\nSaved model to ml/answer_classifier_v2.joblib")