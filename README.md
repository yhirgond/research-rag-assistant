# 📄 Research Paper RAG Assistant

A smart AI-powered assistant that lets you upload research papers (PDFs) and ask questions about them in natural language. The system finds relevant sections from your papers and generates accurate answers with citations.

---

## 🧠 What Does This Do?

Imagine you have 10 research papers and want to know:
- *"What methodology does paper X use?"*
- *"Compare the approaches in these two papers."*
- *"Summarize the key contributions of this paper."*

Instead of reading everything manually, just upload your PDFs and ask — the assistant finds the right sections and answers your question.

---

## 🏗️ How It Works (Architecture)
```
Your Question
      ↓
Convert question to numbers (Embedding)
      ↓
Search through all paper chunks (FAISS Vector DB)
      ↓
Get most relevant sections
      ↓
Send sections + question to AI (OpenAI GPT)
      ↓
Get answer with citations
```

### Components:
- **PDF Parser** — Extracts text from uploaded PDFs page by page
- **Chunker** — Splits text into overlapping chunks using sliding window (LangChain)
- **Embedder** — Converts text chunks into numbers (vectors) using SentenceTransformers
- **Vector Store** — Stores and searches vectors using FAISS
- **LLM Handler** — Sends context + question to OpenAI GPT and gets answer
- **Streamlit UI** — Web interface to upload PDFs and ask questions

---

## 🗂️ Project Structure
```
research-rag-assistant/
├── app.py                        ← Main Streamlit web app
├── requirements.txt              ← All Python dependencies
├── .env                          ← API keys (never commit this!)
├── .gitignore                    ← Files to ignore in Git
├── README.md                     ← This file
│
├── config/
│   └── config.yaml               ← All settings (chunk size, model, top-k etc.)
│
├── data/
│   ├── raw_pdfs/                 ← Upload your PDFs here
│   └── processed/                ← Cleaned text cache
│
├── vectorstore/                  ← FAISS index saved here after indexing
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_parser.py         ← Extracts text from PDFs using PyMuPDF
│   │   ├── chunker.py            ← Splits text into chunks (sliding window)
│   │   └── preprocessor.py      ← Cleans extracted text
│   │
│   ├── embeddings/
│   │   └── embedder.py           ← Converts text to vectors (SentenceTransformers)
│   │
│   ├── retrieval/
│   │   ├── vector_store.py       ← FAISS index: save, load, search
│   │   └── retriever.py          ← Takes query, returns top-k relevant chunks
│   │
│   ├── generation/
│   │   ├── prompt_builder.py     ← Builds prompt with context + question
│   │   └── llm_handler.py        ← Calls OpenAI API and returns answer
│   │
│   └── utils/
│       ├── logger.py             ← Logging setup
│       └── helpers.py            ← Common utility functions
│
├── tests/
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   └── test_generation.py
│
└── notebooks/                    ← Jupyter notebooks for experiments
```

---

## ⚙️ Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.9+ |
| Web UI | Streamlit |
| PDF Parsing | PyMuPDF |
| Text Chunking | LangChain RecursiveCharacterTextSplitter |
| Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Database | FAISS |
| LLM | OpenAI GPT-4o-mini |
| Config | YAML |

---

## 🚀 Installation & Setup

### Step 1 — Clone the repository
```bash
git clone https://github.com/yhirgond/research-rag-assistant.git
cd research-rag-assistant
```

### Step 2 — Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up your OpenAI API key
Create a `.env` file in the root folder:
```
OPENAI_API_KEY=your_openai_api_key_here
```
Get your API key from: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 5 — Run the app
```bash
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

## 📖 How to Use

### 1. Upload Research Papers
- Click **"Browse files"** in the left sidebar
- Select one or more PDF files
- Click **"Index Papers"** button
- Wait for indexing to complete (progress bar will show)

### 2. Ask a Question
- Go to **"Ask a Question"** tab
- Type your question in the text box
- Adjust **Top-K chunks** slider (how many sections to retrieve)
- Click **"Get Answer"**
- View the answer and the source sections used

### 3. Summarize a Paper
- Go to **"Summarize Paper"** tab
- Select a paper from the dropdown
- Click **"Summarize"**
- Get a structured summary with objectives, methodology, findings

---

## 💡 Example Queries
```
"What methodology does this paper use?"
"What are the key contributions of this research?"
"Compare the approaches used in paper A and paper B."
"What dataset was used for training?"
"What are the limitations mentioned in this paper?"
"Summarize the results section."
```

---

## ⚙️ Configuration

Edit `config/config.yaml` to customize the system:
```yaml
chunking:
  chunk_size: 600       # Number of characters per chunk
  chunk_overlap: 100    # Overlap between chunks (sliding window)

embedding:
  model: "all-MiniLM-L6-v2"   # Free local embedding model
  batch_size: 32

retrieval:
  top_k: 5             # Number of chunks to retrieve per query

llm:
  model: "gpt-4o-mini" # OpenAI model to use
  max_tokens: 1000
  temperature: 0.2     # Lower = more factual answers

vectorstore:
  path: "./vectorstore/faiss_index"
```

---

## 🔑 Key Features

- ✅ **Semantic Search** — Finds relevant sections by meaning, not just keywords
- ✅ **Multi-Paper Support** — Index and query across multiple papers at once
- ✅ **Source Citations** — Every answer shows which paper and page it came from
- ✅ **Paper Summarization** — Get structured summaries of any indexed paper
- ✅ **Cross-Paper Comparison** — Compare methodologies across different papers
- ✅ **Sliding Window Chunking** — Preserves context across chunk boundaries

---

## 🛡️ Security Notes

- Never commit your `.env` file — it contains your API key
- The `.gitignore` file already excludes `.env` and `venv/`
- PDF files in `data/raw_pdfs/` are also excluded from Git

---

## 🐛 Common Issues

| Issue | Solution |
|---|---|
| `streamlit: command not found` | Run `source venv/bin/activate` first |
| `OPENAI_API_KEY not found` | Check your `.env` file has the correct key |
| `No papers indexed yet` | Upload PDFs and click "Index Papers" first |
| Slow indexing | Normal for large PDFs — embedding takes time |

---

## 👤 Author

**Yogesh Hirgond**
GitHub: [@yhirgond](https://github.com/yhirgond)

---

## 📜 License

This project is for educational and research purposes.