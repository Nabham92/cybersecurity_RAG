# Cybersecurity RAG

This application allows users to query a corpus of CVE vulnerabilities and generate structured summaries or analytical reports using a Retrieval-Augmented Generation (RAG) system.  
It answers questions by retrieving relevant CVEs and producing clear, security-oriented synthesis outputs.

---

## Technical Stack (RAG)

- **Vector DB:** ChromaDB  
- **Embeddings:** `intfloat/e5-base-v2`  
- **Model:** `gpt-oss:20b` (Ollama Cloud)  
- **Backend API:** FastAPI  
- **UI:** Simple HTML/CSS page served by FastAPI  
- **Pipeline:** retrieval → prompt → generation → display  
- **Containerization:** fully Dockerized for easy deployment  
