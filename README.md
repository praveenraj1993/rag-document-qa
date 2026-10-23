# RAG Document Q&A

Ask questions about your own text documents. The app finds the most relevant parts of your files and an open-source LLM answers using only those parts.

Built with Python, ChromaDB, Ollama (Llama 3.2), FastAPI, pytest and Docker. This is a personal learning project.

## How it works
1. `ingest.py` splits the .txt files in `docs/` into small chunks and stores them in ChromaDB, which creates the embeddings.
2. `POST /ask` searches for the closest chunks to the question.
3. Weak matches are filtered out by a distance cutoff, so the model is not called when nothing relevant is found.
4. The LLM answers only from the retrieved chunks and the API returns the answer with its sources.

## Run locally
1. Install Ollama and run: `ollama pull llama3.2:3b`
2. `pip install -r requirements.txt`
3. Put .txt files in `docs/` and run: `python ingest.py`
4. Start the API: `uvicorn api:app --reload`
5. Open http://127.0.0.1:8000/docs and call `POST /ask`

## Run with Docker
1. Install Ollama and run: `ollama pull llama3.2:3b`
2. `docker build -t rag-document-qa .`
3. `docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 rag-document-qa`
4. Open http://127.0.0.1:8000/docs

## Example
Request: `{"question": "What does the useEffect hook do?"}`
Response: an answer taken from `react.txt` plus `"sources": ["react.txt"]`.
A question outside the documents returns "I can't find that in your documents."

## Tests
`pytest` (the LLM is replaced with a fake, so tests are fast and free)

## Limits and next steps
- Only reads .txt files
- The distance cutoff is tuned by hand on a few questions
- Next: PDF support, chunk overlap, an evaluation set of test questions, and a simple React front end
