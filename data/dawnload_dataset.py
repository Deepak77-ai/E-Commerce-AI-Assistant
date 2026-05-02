from datasets import load_dataset

dataset = load_dataset("NebulaByte/E-Commerce_FAQs", split="train")

df = dataset.to_pandas()

df.to_json("data/ecommerce_faq.json", orient="records", lines=True)

print(df.head())