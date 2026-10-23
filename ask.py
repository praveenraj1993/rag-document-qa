import chromadb
import ollama

collection = chromadb.PersistentClient(path="db").get_or_create_collection("docs")

question = input("Ask: ")
results = collection.query(query_texts=[question], n_results=2)
context = "\n\n".join(results["documents"][0])

reply = ollama.chat(
    model="llama3.2:3b",
    messages=[{"role": "user", "content":
        f"Answer only from this context. If the answer isn't there, say so.\n\nContext:\n{context}\n\nQuestion: {question}"}],
)
print("\n" + reply["message"]["content"])
