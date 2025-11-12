import chromadb
import pandas as pd 

def get_client():
    client=chromadb.PersistentClient()
    return(client)

def intfloat_embedding():
    from chromadb.utils import embedding_functions 
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="intfloat/e5-base-v2",
        device=device
    )
    print(f"Embedding model device : {ef._model.device}")
    return ef

def create_collection(client,name):

    if "logs_corpus" in [c.name for c in client.list_collections()]:
        client.delete_collection("logs_corpus")

    collection = client.get_or_create_collection(name=name,embedding_function=intfloat_embedding())

    return(collection)

def add_to_collection(collection,df : pd.DataFrame):

    ids=[str(i) for i in range(0,len(df))]
    metadatas = [meta if meta is not None else {}for meta in df["meta"].to_list()]

    collection.add(
        ids=ids,
        documents=df["text"].to_list(),
        metadatas=metadatas
    )
    print(f"{len(ids)} documents added.")
    print(collection.peek)

def main():
    from backend.processing import load_data
    from config import COLLECTION_NAME

    df=load_data()
    client=get_client()
    collection=create_collection(client,name=COLLECTION_NAME)

    add_to_collection(collection,df)

if __name__== "__main__":
    main()
