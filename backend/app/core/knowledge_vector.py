import os
from openai import OpenAI, api_key
import chromadb
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import numpy as np

import nltk
import string
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


stop_words = set(stopwords.words('english'))

client = OpenAI(api_key="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")

chroma_client = PersistentClient(path="./chromadb")

embedding_fn = OpenAIEmbeddingFunction(api_key="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", model_name="text-embedding-3-small")

collection = chroma_client.get_or_create_collection(name="knowledge", embedding_function=embedding_fn)


def normalize_query(query: str) -> str:
    """
    Normalize a query by removing stop words and punctuation.

    Args:
        query (str): The input query string.

    Returns:
        str: The normalized query without stop words and punctuation removed.
    """
    tokens = nltk.word_tokenize(query.lower())
    cleaned_tokens = [
        token for token in tokens
        if token not in string.punctuation and token not in stop_words
    ]
    return " ".join(cleaned_tokens)


def mmr(query_embedding, doc_embeddings, lambda_param=0.5, top_n=3):
    """
    Maximal Marginal Relevance (MMR) algorithm.
    """
    selected = []
    remaining = list(range(len(doc_embeddings)))

    doc_sim = np.dot(doc_embeddings, query_embedding)
    doc_sim = doc_sim / (np.linalg.norm(doc_embeddings, axis=1) * np.linalg.norm(query_embedding) + 1e-8)

    while len(selected) < top_n and remaining:
        mmr_score = []
        for i in remaining:
            if not selected:
                diversity_penalty = 0
            else:
                selected_embeds = [doc_embeddings[j] for j in selected]
                redundancy = max([np.dot(doc_embeddings[i], doc_embeddings[j]) /
                                  (np.linalg.norm(doc_embeddings[i]) * np.linalg.norm(doc_embeddings[j]) + 1e-8)
                                  for j in selected])
                diversity_penalty = redundancy

            score = lambda_param * doc_sim[i] - (1 - lambda_param) * diversity_penalty
            mmr_score.append(score)

        next_idx = remaining[np.argmax(mmr_score)]
        selected.append(next_idx)
        remaining.remove(next_idx)

    return selected


def add_knowledge_chunks(topic: str, chunks: list[str]):
    ids = [f"{topic}-{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, metadatas=[{"topic": topic} for _ in chunks], ids=ids)


def search_knowledge_vector(query: str, top_k: int = 5) -> list[str]:
    """
    Searches the vector store for knowledge chunks most relevant to the query using MMR selection.

    Args:
        query (str): The user's natural language question.
        top_k (int, optional): Number of initial results to retrieve from the vector store. Defaults to 5.

    Returns:
        list[str]: A list of top relevant text chunks selected using MMR.
    """
    query = normalize_query(query)
    #print(query)
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "distances", "embeddings"]
    )
    
    if not results["documents"] or not results["documents"][0]:
        return []
    
    documents = results["documents"][0]
    embeddings = np.array(results["embeddings"][0])
    query_embed = collection._embedding_function(query)[0]

    selected_indices = mmr(query_embed, embeddings, 0.5, 3)

    return [documents[i] for i in selected_indices]
