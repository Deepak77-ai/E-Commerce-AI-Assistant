import os
from pathlib import Path

import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

MODEL_FOLDER = os.getenv("TRAINED_MODEL_PATH", "model/flan-t5-ecommerce")

MAX_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "120"))

MODEL_PATH = BASE_DIR / MODEL_FOLDER



if not MODEL_PATH.exists():
    raise RuntimeError(
        f"Trained model not found at: {MODEL_PATH}\n"
        "Please run:  python train_model.py"
    )



tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

model.eval()



def ask_model(question: str) -> dict:
    """
    Send a question to the AI model and get an answer back.

    Args:
        question: The customer's question as plain text.

    Returns:
        A dict like {"answer": "Your answer here"}
    """

    question = question.strip()

    # Return early if the question is empty
    if not question:
        return {"answer": "Please enter a valid question."}

    # Build the full prompt that the model receives
    prompt = (
        "You are an e-commerce customer support assistant. "
        f"Question: {question}"
    )

    # Convert the prompt text into numbers the model understands
    inputs = tokenizer(
        prompt,
        return_tensors="pt",   # PyTorch tensors
        truncation=True,       # Cut off if too long
        padding=True,          # Pad if too short
        max_length=256,        # Max input length
    ).to(device)

    # Generate the answer (no gradient tracking needed — saves memory)
    with torch.no_grad():
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=MAX_TOKENS,  # Max answer length
            num_beams=4,                # Beam search: considers 4 options at once
            early_stopping=True,        # Stop once all beams finish
        )

    # Convert the output numbers back to readable text
    answer = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

    return {"answer": answer}