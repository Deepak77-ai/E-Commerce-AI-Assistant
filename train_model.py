import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import Trainer, TrainingArguments

model_name = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

df = pd.read_json("data/ecommerce_faq.json", lines=True)

df["text"] = df["que_ans"]

dataset = Dataset.from_pandas(df[["text"]])

def tokenize(example):
    tokens = tokenizer(
        example["text"],
        padding="max_length",
        truncation=True,
        max_length=128
    )
    
    tokens["labels"] = tokens["input_ids"].copy()
    
    return tokens

dataset = dataset.map(tokenize)

dataset = dataset.remove_columns(["text"])

training_args = TrainingArguments(
    output_dir="model",
    num_train_epochs=3,
    per_device_train_batch_size=2,
    logging_steps=10,
    save_steps=50
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

trainer.train()

model.save_pretrained("model")
tokenizer.save_pretrained("model")