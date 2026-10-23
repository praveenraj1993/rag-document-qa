import chromadb

client = chromadb.PersistentClient(path="db")
collection = client.get_or_create_collection("docs")

question = input("Ask: ")
results = collection.query(query_texts=[question], n_results=2)

for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
    print("\nFrom", meta["source"], ":")
    print(doc)
