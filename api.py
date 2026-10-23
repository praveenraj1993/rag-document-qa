import chromadb
import ollama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
collection = chromadb.PersistentClient(path="db").get_or_create_collection("docs")

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    results = collection.query(query_texts=[q.question], n_results=2)
    context = "\n\n".join(results["documents"][0])
    sources = [m["source"] for m in results["metadatas"][0]]
    reply = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content":
            f"Answer only from this context. If the answer isn't there, say so.\n\nContext:\n{context}\n\nQuestion: {q.question}"}],
    )
    return {"answer": reply["message"]["content"], "sources": sources}
