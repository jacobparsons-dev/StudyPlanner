import numpy as np
import pandas as pd
import joblib

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import(
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
data = pd.read_csv("ml/answer_training_data.csv")

print(f"Loaded {len(data)} training examples")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def create_features(expected_answers,student_answers):
    """
    Turn each expected/student answer pair into numerical features
    that classifier can learn from
    """
    expected_embeddings = embedding_model.encode(
        expected_answers.tolist(),
        convert_to_numpy= True,
    )
    student_embeddings = embedding_model.encode(
        student_answers.tolist(),
        convert_to_numpy=True,
    )
    # How different
    difference = np.abs(
        expected_embeddings - student_embeddings
    )
    # Where do they agree
    interaction = (
        expected_embeddings * student_embeddings
    )
    # combine feature sets
    return np.concatenate(
        [difference, interaction],
        axis=1
    )
X = create_features(
    data["expected_answer"],
    data["student_answer"],
)
y = data["label"].values

print(f"Feature matrix shape: {X.shape}")

# Split examples into training and test data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

classifier = LogisticRegression(
    max_iter=1000
)
classifier.fit(X_train, y_train)

# test on answers the classifier wasn't trained on
predictions = classifier.predict(X_test)

print("\nModel evaluation")
print(f"Accuracy:  {accuracy_score(y_test, predictions):.3f}")
print(f"Precision: {precision_score(y_test, predictions):.3f}")
print(f"Recall:    {recall_score(y_test, predictions):.3f}")
print(f"F1 score:  {f1_score(y_test, predictions):.3f}")

print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions))

# save the trained classifier
joblib.dump(
    classifier,
    "ml/answer_classifier.joblib"
)
print("\nSaved model to ml/answer_classifier.joblib")