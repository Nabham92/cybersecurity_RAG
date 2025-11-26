import chromadb
from chromadb.config import Settings
from backend.config import COLLECTION_NAME
import os 
from dotenv import load_dotenv
from backend.app.database.embeddings import intfloat_embedding

load_dotenv()

def get_chroma_client() -> chromadb.Client:

    host = os.getenv("CHROMA_HOST")
    port = os.getenv("CHROMA_PORT")

    settings=Settings(chroma_server_host=host,
                      chroma_server_http_port=port)
    
    client = chromadb.HttpClient(host=settings.chroma_server_host,
                                 port=settings.chroma_server_http_port,
                                 settings=settings)
    
    return(client)

EMBED_FUNC = intfloat_embedding()

def get_collection(client, collection_name):
    return client.get_collection(collection_name, embedding_function=EMBED_FUNC)
