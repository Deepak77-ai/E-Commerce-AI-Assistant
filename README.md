# 🛍️ E-Commerce AI Assistant

> A locally-running AI-powered customer support chatbot for e-commerce. Built with a fine-tuned **flan-t5** model and a **FastAPI** backend — handles questions about orders, delivery, returns, refunds, and account issues entirely on your machine.

<img width="1882" height="958" alt="image" src="https://github.com/user-attachments/assets/618013b7-2c6c-4cea-8117-8b8b15b5ca7d" />


---

## ✨ Features

- 💬 **AI Chat** — answers e-commerce support questions using a fine-tuned `flan-t5` model
- 📦 **Order Tracking** — look up mock order statuses by order ID
- ⚡ **FastAPI Backend** — lightweight REST API with auto-generated `/docs` page
- 🖥️ **Vanilla Frontend** — plain HTML, CSS, and JavaScript — no framework needed
- 🔒 **Fully Local** — no external API calls, no data sent anywhere

---

## 🗂️ Project Structure

```
ecommerce-ai-assistant/
│
├── backend/
│   ├── main.py               # FastAPI app, routes, CORS
│   ├── inference.py          # Loads the model, runs ask_model()
│   └── orders.py             # Mock order lookup (track_order)
│
├── data/
│   └── dawnload_dataset.py   # Downloads FAQ dataset from Hugging Face
│
├── frontend/
│   ├── index.html            # Chat UI
│   ├── script.js             # Handles chat & order tracking requests
│   └── style.css             # Styles
│
├── train_model.py            # Fine-tunes flan-t5 on the FAQ dataset
├── requirements.txt          # Python dependencies
└── .env                      # Configuration (model paths, settings)
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ecommerce-ai-assistant.git
cd ecommerce-ai-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure `.env`

Create a `.env` file in the project root:

```env
APP_NAME=E-Commerce AI Assistant

BASE_MODEL_NAME=google/flan-t5-small
TRAINED_MODEL_PATH=model/flan-t5-ecommerce
FAQ_DATA_PATH=data/ecommerce_faq.json

MAX_NEW_TOKENS=120
```

---

## 🚀 Running the Project

Follow these steps **in order** the first time you run the project.

### Step 1 — Download the dataset

Downloads the [NebulaByte/E-Commerce_FAQs](https://huggingface.co/datasets/NebulaByte/E-Commerce_FAQs) dataset from Hugging Face and saves it to `data/ecommerce_faq.json`.

```bash
python data/dawnload_dataset.py
```

### Step 2 — Train the model

Fine-tunes `google/flan-t5-small` on the FAQ dataset and saves the trained model to `model/flan-t5-ecommerce/`. This may take a few minutes depending on your hardware.

```bash
python train_model.py
```

### Step 3 — Start the server

```bash
uvicorn backend.main:app --reload
```

### Step 4 — Open the app

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the frontend chat UI |
| `POST` | `/api/chat` | Sends a question, returns an AI answer |
| `GET` | `/api/order/{order_id}` | Looks up an order by ID |

**Chat request:**
```json
{ "question": "What is your return policy?" }
```

**Chat response:**
```json
{ "answer": "You can return items within 30 days of purchase..." }
```

**Order tracking response:**
```json
{
  "found": true,
  "order_id": "ORD123",
  "status": "Out for delivery",
  "expected_delivery": "Today",
  "message": "Your order is out for delivery."
}
```

**Sample order IDs for testing:** `ORD123`, `ORD456`, `ORD789`

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| AI Model | [google/flan-t5-small](https://huggingface.co/google/flan-t5-small) via 🤗 Transformers |
| Training Data | [NebulaByte/E-Commerce_FAQs](https://huggingface.co/datasets/NebulaByte/E-Commerce_FAQs) |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| Frontend | HTML + CSS + Vanilla JavaScript |
| Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |

---

## 💡 Want Better Answers?

Swap `google/flan-t5-small` for a larger model in your `.env`:

```env
BASE_MODEL_NAME=google/flan-t5-base    # better answers, needs more RAM
BASE_MODEL_NAME=google/flan-t5-large   # best answers, needs a GPU
```

Then re-run `train_model.py` to retrain on the new base model.

---

## 📄 License

MIT
