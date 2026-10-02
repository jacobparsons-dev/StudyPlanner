from pathlib import Path

import numpy as np
import pandas as pd
import torch 

from datasets import Dataset
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import GroupShuffleSplit
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

ML_DIR = Path(__file__).resolve().parent

DATA_PATH = ML_DIR / "answer_training_data_v2.csv"
MODEL_OUTPUT = ML_DIR / "answer_grading_transformer"

data = pd.read_csv(DATA_PATH)

print(f"Loaded {len(data)} examples")
print(f"Questions: {data['question_id'].nunique()}")

groups = data["question_id"].values

# Roughly 70% training, 30% validation/test
first_split = GroupShuffleSplit(
    n_splits=1,
    test_size=0.30,
    random_state=42,
)

train_idx, temp_idx = next(
    first_split.split(
        data,
        data["label"],
        groups,
    )
)

train_data = data.iloc[
    train_idx
].reset_index(drop=True)

temp_data = data.iloc[
    temp_idx
].reset_index(drop=True)


# Split remaining data into validation and test sets
second_split = GroupShuffleSplit(
    n_splits=1,
    test_size=0.50,
    random_state=42,
)

temp_groups = temp_data["question_id"].values

validation_idx, test_idx = next(
    second_split.split(
        temp_data,
        temp_data["label"],
        temp_groups,
    )
)

validation_data = temp_data.iloc[
    validation_idx
].reset_index(drop=True)

test_data = temp_data.iloc[
    test_idx
].reset_index(drop=True)



train_questions = set(
    train_data["question_id"]
)

validation_questions = set(
    validation_data["question_id"]
)

test_questions = set(
    test_data["question_id"]
)


assert train_questions.isdisjoint(
    validation_questions
)

assert train_questions.isdisjoint(
    test_questions
)

assert validation_questions.isdisjoint(
    test_questions
)


print("\nDataset split")
print("-------------")

print(
    f"Training:   {len(train_data)} examples "
    f"({len(train_questions)} questions)"
)

print(
    f"Validation: {len(validation_data)} examples "
    f"({len(validation_questions)} questions)"
)

print(
    f"Test:       {len(test_data)} examples "
    f"({len(test_questions)} questions)"
)

print("Question overlap: 0")


def build_text(row):
    return (
        f"Question: {row['question']} "
        f"Expected answer: {row['expected_answer']} "
        f"Student answer: {row['student_answer']}"
    )


train_data["text"] = train_data.apply(
    build_text,
    axis=1,
)

validation_data["text"] = validation_data.apply(
    build_text,
    axis=1,
)

test_data["text"] = test_data.apply(
    build_text,
    axis=1,
)

train_dataset = Dataset.from_pandas(
    train_data[["text", "label"]]
)

validation_dataset = Dataset.from_pandas(
    validation_data[["text", "label"]]
)

test_dataset = Dataset.from_pandas(
    test_data[["text", "label"]]
)

MODEL_NAME = "distilbert-base-uncased"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)


def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        padding="max_length",
        max_length=192,
    )


train_dataset = train_dataset.map(
    tokenize,
    batched=True,
)

validation_dataset = validation_dataset.map(
    tokenize,
    batched=True,
)

test_dataset = test_dataset.map(
    tokenize,
    batched=True,
)

id2label = {
    0: "incorrect",
    1: "partial",
    2: "correct",
}

label2id = {
    "incorrect": 0,
    "partial": 1,
    "correct": 2,
}


model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3,
    id2label=id2label,
    label2id=label2id,
)


def compute_metrics(eval_prediction):
    logits, labels = eval_prediction

    predictions = np.argmax(
        logits,
        axis=-1,
    )

    accuracy = accuracy_score(
        labels,
        predictions,
    )

    macro_f1 = f1_score(
        labels,
        predictions,
        average="macro",
    )

    return {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
    }


training_args = TrainingArguments(
    output_dir=str(
        ML_DIR / "transformer_checkpoints"
    ),

    num_train_epochs=5,

    per_device_train_batch_size=8,
    per_device_eval_batch_size=16,

    learning_rate=2e-5,
    weight_decay=0.01,

    eval_strategy="epoch",
    save_strategy="epoch",

    load_best_model_at_end=True,

    metric_for_best_model="macro_f1",
    greater_is_better=True,

    save_total_limit=1,

    logging_steps=10,

    report_to="none",
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=validation_dataset,
    compute_metrics=compute_metrics,
)

print("\nStarting transformer training...")

device = (
    "GPU"
    if torch.cuda.is_available()
    else "CPU"
)

print(f"Running on: {device}")

if torch.cuda.is_available():
    print(
        f"GPU: {torch.cuda.get_device_name(0)}"
    )


trainer.train()

print("\nFinal test evaluation")
print("---------------------")

test_output = trainer.predict(
    test_dataset
)

test_predictions = np.argmax(
    test_output.predictions,
    axis=-1,
)

test_labels = test_data[
    "label"
].values


accuracy = accuracy_score(
    test_labels,
    test_predictions,
)

macro_f1 = f1_score(
    test_labels,
    test_predictions,
    average="macro",
)


print(
    f"Accuracy: {accuracy:.3f}"
)

print(
    f"Macro F1: {macro_f1:.3f}"
)


print("\nClassification report:")

print(
    classification_report(
        test_labels,
        test_predictions,
        target_names=[
            "incorrect",
            "partial",
            "correct",
        ],
        digits=3,
    )
)


print("Confusion matrix:")

print(
    confusion_matrix(
        test_labels,
        test_predictions,
    )
)

trainer.save_model(
    str(MODEL_OUTPUT)
)

tokenizer.save_pretrained(
    str(MODEL_OUTPUT)
)


print(
    "\nSaved transformer model to:"
)

print(MODEL_OUTPUT)