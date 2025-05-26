✅ README.md
# 📚 RAG (Retrieval-Augmented Generation) with LLaMA 3.2 and Ollama

This project is a simple and powerful Retrieval-Augmented Generation (RAG) system built using:

- 🧠 LLaMA 3.2 via [Ollama](https://ollama.com/)
- 📚 LangChain for orchestration
- 🔍 BGE-large embeddings (`BAAI/bge-large-en`)
- 🗃️ ChromaDB for vector search
- 🐍 Python

It allows you to ask questions based on your own documents (PDFs) using a local LLM.

---

## 🚀 Quickstart

### 1. 🖥️ Clone the Repository

```bash
git clone https://github.com/SAHILBODKHE/RAGs.git
cd RAGs
2. 🧠 Install Ollama and Pull LLaMA 3.2
📥 Install Ollama (macOS, Linux, Windows):
👉 https://ollama.com/download
⚠️ You must run Ollama in the background before using the model.
🧠 Pull the LLaMA 3.2 Model
ollama pull llama3.2
3. 🐍 Create a Virtual Environment & Install Dependencies
python3 -m venv .venv
source .venv/bin/activate           # For Windows: .venv\Scripts\activate
pip install -r requirements.txt
4. 📂 Add Your PDFs
Place any PDF documents you want to ask questions about inside the data/ folder.
5. 📦 Ingest the Data into ChromaDB
This step processes your documents and saves their embeddings for semantic search.
python ingest.py
6. 💬 Ask Questions (RAG in Action)
# In one terminal
ollama run llama3.2:latest

# In another terminal (after activating the virtual environment):
python rag.py
Then ask anything! Example:
❓ Ask a question: What are the mandatory procedures for academic proctors?
🛠️ File Structure

├── data/                 ← PDF documents
├── db/                   ← Vector database (auto-created)
├── embeddings.py         ← Loads BGE embeddings
├── ingest.py             ← PDF processing + ChromaDB storage
├── llama_model.py        ← Communicates with Ollama
├── rag.py                ← Runs the main RAG loop
├── retriever.py          ← Finds relevant chunks from DB
├── requirements.txt      ← Python dependencies
└── .gitignore            ← Ignores .venv, db, models, etc.
⚠️ Troubleshooting

❌ KeyError: 'response': Check that your model name in llama_model.py matches the name shown in ollama list
❌ GitHub file size errors: Use .gitignore to exclude .venv/, models, and Chroma DB files
❌ NumPy errors: Use numpy<2.0.0 in requirements.txt for compatibility with PyTorch, Transformers, etc.
✨ Future Improvements

Add a FastAPI or Streamlit web UI
Connect to Qdrant instead of Chroma
Use LangChain agents for tool use
Add source citations for each answer
📜 License

MIT – Use it, modify it, share it.
Built with ❤️ by Sahil Bodkhe
MEng Systems Design Engineering, University of Waterloo
