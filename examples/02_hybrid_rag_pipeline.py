"""
Pattern 02: Hybrid RAG Search with Reciprocal Rank Fusion (RRF)
Combines keyword (BM25) and dense vector retrieval for high-accuracy context selection.
"""

from collections import defaultdict
from typing import List, Dict

def reciprocal_rank_fusion(dense_rankings: List[str], sparse_rankings: List[str], k: int = 60) -> List[tuple]:
    scores = defaultdict(float)
    
    for rank, doc_id in enumerate(dense_rankings):
        scores[doc_id] += 1.0 / (k + rank + 1)
        
    for rank, doc_id in enumerate(sparse_rankings):
        scores[doc_id] += 1.0 / (k + rank + 1)
        
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)

if __name__ == "__main__":
    dense_results = ["doc_postgres_pgvector", "doc_agent_memory", "doc_rag_chunking"]
    sparse_results = ["doc_rag_chunking", "doc_postgres_pgvector", "doc_redis_cache"]
    
    fused = reciprocal_rank_fusion(dense_results, sparse_results)
    print("Reciprocal Rank Fusion (RRF) Scoring:")
    for rank, (doc, score) in enumerate(fused, start=1):
        print(f"Rank {rank}: {doc} (Score: {score:.5f})")
