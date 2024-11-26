import numpy as np
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.utils.math import cosine_similarity

keywords_api = ["Astronomy", "Space", "NASA", "Hubble", "Galaxy", "Nebula", "Stars", "Planets", "Universe", "Spacecraft", "Astrophotography",
                "Astronomía", "Espacio", "NASA", "Hubble", "Galaxia", "Nebulosa", "Estrellas", "Planetas", "Universo", "Sonda espacial", "Astrofotografía"]

def load_embedding_model(model_path: str = "../models/nomic-embed-text-v1.5.Q4_K_M.gguf") -> LlamaCppEmbeddings:
    return LlamaCppEmbeddings(model_path=model_path)

def is_api_request(question: str, keywords: list, threshold: float = 0.7) -> bool:
    embedding_model = load_embedding_model()
    embed_keywords = [embedding_model.embed_query(key) for key in keywords]
    embed_question = embedding_model.embed_query(question)
    similarities = [cosine_similarity(embed_question, api_emb) for api_emb in embed_keywords] 
    max_similarity = np.max(similarities) 
    return max_similarity > threshold
    