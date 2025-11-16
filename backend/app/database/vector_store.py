import chromadb
from chromadb.config import Settings
from config import COLLECTION_NAME

def get_chroma_client() -> chromadb.Client:

    settings=Settings(chroma_server_host="localhost",
                      chroma_server_http_port="8000")
    
    client = chromadb.HttpClient(settings=settings)
    
    return(client)

def get_collection(client,collection_name):

    collection=client.get_collection(collection_name)
    print(f"Collection {collection_name} loaded")
    return(collection)
