FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "from chromadb.utils.embedding_functions import ONNXMiniLM_L6_V2; ONNXMiniLM_L6_V2()(['warm up'])"
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "python ingest.py && uvicorn api:app --host 0.0.0.0 --port 8000"]
