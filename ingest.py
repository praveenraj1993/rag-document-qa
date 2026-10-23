import os
import chromadb

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("docs")

def chunk(text, size=80):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]

for name in os.listdir("docs"):
    if not name.endswith(".txt"):
        continue
    text = open(f"docs/{name}").read()
    for i, c in enumerate(chunk(text)):
        collection.add(documents=[c], ids=[f"{name}-{i}"], metadatas=[{"source": name}])

print("done:", collection.count(), "chunks")
