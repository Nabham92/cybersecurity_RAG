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