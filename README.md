
## Run with Docker
1. Install Ollama and run: ollama pull llama3.2:3b
2. docker build -t rag-document-qa .
3. docker run -p 8000:8000 -e OLLAMA_HOST=http://host.docker.internal:11434 rag-document-qa
4. Open http://127.0.0.1:8000/docs

## Tests
pytest
