pip install -r requirements.txt


1.Ingestion 
PYTHONPATH=. python3 embed_schema.py

Chroma_db created then

2. Run main.py
PYTHONPATH=. uvicorn api.main:app --reload

3.run your ollama llama 3.2

4.Test it with test query set
python3 test_queries.py




