from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("model")

tokenizer.pad_token = tokenizer.eos_token   # add this line here

model = AutoModelForCausalLM.from_pretrained("model")

def ask_model(question):

    prompt = f"Question: {question} Answer:"

    inputs = tokenizer(prompt, return_tensors="pt")

    outputs = model.generate(
        **inputs,
        max_length=100
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return response