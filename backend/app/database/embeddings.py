from chromadb.api.types import EmbeddingFunction, Documents, Embeddings
from sentence_transformers import SentenceTransformer
import torch

# Load the model ONCE globally

_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
_GLOBAL_MODEL = SentenceTransformer("intfloat/e5-base-v2", device=_DEVICE)


class E5EmbeddingFunction(EmbeddingFunction):
    def __init__(self, model_name="intfloat/e5-base-v2"):
        super().__init__()
        self.model_name = model_name

        # 🟦 Instead of reloading, reuse the global instance
        self.model = _GLOBAL_MODEL

    def __call__(self, input: Documents) -> Embeddings:
        # encode with the SINGLE loaded model
        return self.model.encode(input, convert_to_numpy=True).tolist()

    def name(self) -> str:
        return self.model_name


def intfloat_embedding():
    return E5EmbeddingFunction()
