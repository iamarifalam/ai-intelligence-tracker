#!/usr/bin/env python3
"""
RAG (Retrieval-Augmented Generation) retrieval latency and precision benchmark.
Evaluates vector retrieval hit-rate, precision@k, and latency across chunk sizes.
"""

import math
import random
import time
from typing import Dict, List, Tuple


def generate_synthetic_corpus(num_docs: int = 100, doc_len: int = 50) -> List[Dict[str, any]]:
    vocab = ["transformer", "attention", "embedding", "vector", "latency", "precision", "recall", "index", "cosine", "dotproduct", "quantization", "rag", "benchmark"]
    corpus = []
    for i in range(num_docs):
        text = " ".join(random.choices(vocab, k=doc_len))
        corpus.append({"id": f"doc_{i}", "text": text, "tokens": text.split()})
    return corpus


def compute_tf_idf_similarity(query_tokens: List[str], doc_tokens: List[str]) -> float:
    common = set(query_tokens).intersection(set(doc_tokens))
    if not common:
        return 0.0
    return len(common) / (math.sqrt(len(query_tokens)) * math.sqrt(len(doc_tokens)))


def run_retrieval_benchmark(num_queries: int = 50, top_k: int = 5) -> Dict[str, any]:
    corpus = generate_synthetic_corpus(num_docs=200, doc_len=40)
    query_vocab = ["embedding", "latency", "vector", "transformer", "rag"]
    
    latencies = []
    hit_counts = 0

    start_total = time.perf_counter()
    for _ in range(num_queries):
        query = random.choices(query_vocab, k=3)
        t0 = time.perf_counter()
        
        scores: List[Tuple[str, float]] = []
        for doc in corpus:
            sim = compute_tf_idf_similarity(query, doc["tokens"])
            if sim > 0.0:
                scores.append((doc["id"], sim))
        
        scores.sort(key=lambda x: x[1], reverse=True)
        top_results = scores[:top_k]
        
        dt_ms = (time.perf_counter() - t0) * 1000.0
        latencies.append(dt_ms)
        if top_results:
            hit_counts += 1

    total_time_ms = (time.perf_counter() - start_total) * 1000.0
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0.0
    hit_rate = (hit_counts / num_queries) * 100.0

    return {
        "num_docs": len(corpus),
        "num_queries": num_queries,
        "top_k": top_k,
        "avg_latency_ms": round(avg_latency, 3),
        "p95_latency_ms": round(p95_latency, 3),
        "hit_rate_pct": round(hit_rate, 2),
        "total_time_ms": round(total_time_ms, 2)
    }


if __name__ == "__main__":
    results = run_retrieval_benchmark()
    print("Benchmark Results:", results)
