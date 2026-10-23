import chromadb
import ollama
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
collection = chromadb.PersistentClient(path="db").get_or_create_collection("docs")

MAX_DISTANCE = 1.3

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Question):
    results = collection.query(query_texts=[q.question], n_results=3)
    # print(results["distances"][0])

    if results["distances"][0][0] > MAX_DISTANCE:
        return {"answer": "I can't find that in your documents.", "sources": []}

    keep = [i for i, d in enumerate(results["distances"][0]) if d <= MAX_DISTANCE]
    context = "\n\n".join(results["documents"][0][i] for i in keep)
    sources = [results["metadatas"][0][i]["source"] for i in keep]
    reply = ollama.chat(
        model="llama3.2:3b",
        messages=[{"role": "user", "content":
            f"Use ONLY the context below. Do not use any outside knowledge. If the answer is not in the context, say you don't know.\n\nContext:\n{context}\n\nQuestion: {q.question}"}],
    )
    return {"answer": reply["message"]["content"], "sources": sources}
