import chromadb
from chromadb.config import Settings
import pandas as pd 
from backend.app.database.embeddings import intfloat_embedding
from backend.app.database.vector_store import get_chroma_client

def create_chroma_collection(client,collection_name,embedding_function=None):

    existing_names=[collection.name  for collection in client.list_collections() ]

    if collection_name not in existing_names : 
        collection=client.create_collection(collection_name,embedding_function=embedding_function)
        print(f"Collection {collection_name} created.")
        
    else : 
        collection=client.get_collection(collection_name)
        print(f"Collection {collection_name} already exists")

    return(collection)

def add_to_collection(collection,df : pd.DataFrame):

    ids=[str(i) for i in range(0,len(df))]
    metadatas = [meta if meta is not None else {} for meta in df["meta"].to_list()]

    collection.add(
        ids=ids,
        documents=df["text"].to_list(),
        metadatas=metadatas
    )
    print(f"{len(ids)} documents added.",f"Collection length : {collection.count()} documents")
    print(collection.peek)

def main():
    from backend.app.database.processing import load_data
    from config import COLLECTION_NAME

    df=load_data()
    client=get_chroma_client()
    collection=create_chroma_collection(client,COLLECTION_NAME,embedding_function=intfloat_embedding)
    
    add_to_collection(collection,df)

if __name__== "__main__":
    main()
