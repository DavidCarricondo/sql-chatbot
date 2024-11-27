import numpy as np
from langchain_community.embeddings import LlamaCppEmbeddings
from langchain_community.utils.math import cosine_similarity

keywords_api = ["Astronomy", "Space", "NASA", "Hubble", "Galaxy", "Nebula", "Stars", "Planets", "Universe", "Spacecraft", "Astrophotography", "picture",
                "Astronomía", "Espacio", "NASA", "Hubble", "Galaxia", "Nebulosa", "Estrellas", "Planetas", "Universo", "Sonda espacial", "Astrofotografía", "imagen"]

def load_embedding_model(model_path: str = "../models/nomic-embed-text-v1.5.Q4_K_M.gguf") -> LlamaCppEmbeddings:
    return LlamaCppEmbeddings(model_path=model_path)

def is_api_request(question: str, keywords: list = keywords_api, threshold: float = 0.6) -> bool:
    ##TODO cache keyword embeddings
    embedding_model = load_embedding_model()
    embed_keywords = [embedding_model.embed_query(key.lower()) for key in keywords]
    embed_keywords = [np.array(key).reshape(1,-1) for key in embed_keywords]

    embed_question = embedding_model.embed_query(question.lower())
    embed_question = np.array(embed_question).reshape(1, -1)

    similarities = [cosine_similarity(embed_question, api_emb) for api_emb in embed_keywords] 
    max_similarity = np.max(similarities) 
    return max_similarity > threshold
    
if __name__ == "__main__": 

    question = "Dame la última imagen de la NASA"#"cuantos clientes compraron por más de 3000 en importe" #"Dame la última imagen de la NASA"
    print(is_api_request(question)) 
