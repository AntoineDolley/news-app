# app/utils/clustering.py
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import defaultdict
from app.models import Article  # Assurez-vous que le chemin est correct
import json
from .utils.openai import generate_summary_and_title_async
import asyncio

def workflow_query_cluster_and_summarize(articles, k_range: range = range(2, 21)):
    data = []
    for art in articles:
        embedding_array = np.array(art.embedding) if art.embedding else None
        data.append({
            'id': art.id,
            'title': art.title,
            'summary': art.summary,
            'raw_text': art.raw_text,
            'published_at': art.published_at,
            'url': art.url,
            'embedding': embedding_array
        })

    df = pd.DataFrame(data)

    # Nettoyer et convertir les embeddings
    df['embedding'] = df['embedding'].apply(fix_ndarray_embeddings)
    df = df.dropna(subset=['embedding'])  # Supprimer les lignes sans embeddings
    embeddings = np.vstack(df['embedding'].values)

    # Trouver le k optimal pour K-Means
    sse = []
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(embeddings)
        sse.append(kmeans.inertia_)

    def find_optimal_k(sse, k_range):
        sse_diff = np.diff(sse)
        sse_diff_2 = np.diff(sse_diff)
        optimal_k_index = np.argmax(np.abs(sse_diff_2)) + 1
        return k_range[optimal_k_index]

    k_optimal = find_optimal_k(sse, k_range)

    # Appliquer K-Means avec k optimal
    kmeans = KMeans(n_clusters=k_optimal, random_state=42)
    df['cluster'] = kmeans.fit_predict(embeddings)

    # Gérer l'asynchronisme dans une boucle d'événements locale
    def perform_summarization(df):
        async def process_clusters():
            cluster_summaries = {}
            tasks = []
            for cluster_id in sorted(df['cluster'].unique()):
                cluster_text = " ".join(df[df['cluster'] == cluster_id]['raw_text'])
                tasks.append(generate_summary_and_title_async(cluster_text, cluster_id))

            results = await asyncio.gather(*tasks)
            for cluster_id, summary_and_title in results:
                cluster_summaries[cluster_id] = {
                    "title": summary_and_title.get("title", f"Cluster {cluster_id}"),
                    "summary": summary_and_title.get("summary", "No summary available."),
                    "articles": df[df['cluster'] == cluster_id].to_dict(orient='records')
                }
            return cluster_summaries

        # Lancer une boucle d'événement locale
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(process_clusters())
        finally:
            loop.close()

    cluster_summaries = perform_summarization(df)
    return cluster_summaries

def fix_ndarray_embeddings(embedding):
    """
    Corrige un numpy.ndarray contenant des listes de nombres.
    Convertit tout en tableau NumPy de floats.
    """
    try:
        if isinstance(embedding, np.ndarray) and embedding.ndim == 0:
            return np.array(json.loads(embedding.item()), dtype=float)
        if isinstance(embedding, np.ndarray) and embedding.size == 1 and isinstance(embedding[0], str):
            return np.array(json.loads(embedding[0]), dtype=float)
        if isinstance(embedding, np.ndarray) and embedding.dtype in [np.float32, np.float64]:
            return embedding
        if isinstance(embedding, str):
            return np.array(json.loads(embedding), dtype=float)
    except Exception as e:
        print(f"Erreur lors du traitement : {e}, embedding : {embedding}")
        return None
    
    print(f"Embedding invalide ou type inattendu : {type(embedding)}")
    return None
