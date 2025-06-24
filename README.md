# 📄 Intelligent File QA Chatbot

This application allows users to upload documents and interact with them using a chat interface powered by embeddings, a vector database, and a Large Language Model (LLM).

## 🧠 Architecture Overview

```mermaid
graph TB
    A[User Uploads File] --> B[Text Extraction]
    B --> C[Chunking & Embedding]
    C --> D[Vector Database]
    D --> E[Chat Interface]
    E --> F[Query Processing]
    F --> D
    D --> G[LLM Generation]
    G --> E
