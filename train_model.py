import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Trainer,
    TrainingArguments,
)



BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

BASE_MODEL_NAME = os.getenv("BASE_MODEL_NAME", "google/flan-t5-small")

FAQ_DATA_PATH = os.getenv("FAQ_DATA_PATH", "data/ecommerce_faq.json")

TRAINED_MODEL_PATH = os.getenv("TRAINED_MODEL_PATH", "model/flan-t5-ecommerce")

DATA_PATH = BASE_DIR / FAQ_DATA_PATH
OUTPUT_DIR = BASE_DIR / TRAINED_MODEL_PATH

print("Loading base model:", BASE_MODEL_NAME)
print("Loading dataset:", DATA_PATH)


tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(BASE_MODEL_NAME)



df = pd.read_json(DATA_PATH, lines=True)

for column in ["question", "answer"]:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

df = df.dropna(subset=["question", "answer"])


def build_input(row):
    """
    Turn one FAQ row into a full prompt string for the model.
    Uses the "category" column if available, otherwise defaults to "General".

    Example output:
        "You are an e-commerce customer support assistant.
         Category: Returns. Question: How do I return an item?"
    """
    category = row.get("category", "General")
    return (
        "You are an e-commerce customer support assistant. "
        f"Category: {category}. "
        f"Question: {row['question']}"
    )

df["input_text"] = df.apply(build_input, axis=1)

df["target_text"] = df["answer"].astype(str)


dataset = Dataset.from_pandas(df[["input_text", "target_text"]])



def preprocess(example):
    """
    Convert text strings into token ID numbers that the model can train on.
    Both the input (question/prompt) and the label (answer) are tokenized.
    """
    model_inputs = tokenizer(
        example["input_text"],
        max_length=256,   
        truncation=True,
    )

    labels = tokenizer(
        text_target=example["target_text"],
        max_length=256,
        truncation=True,
    )

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess, batched=True)



data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
)



training_args = TrainingArguments(
    output_dir=str(OUTPUT_DIR),       
    num_train_epochs=3,               
    per_device_train_batch_size=4,    
    learning_rate=5e-5,               
    logging_steps=20,                 
    save_strategy="epoch",            
    save_total_limit=2,               
    report_to="none",                 



trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
)

trainer.train()



model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Training complete.")
print("Model saved at:", OUTPUT_DIR)