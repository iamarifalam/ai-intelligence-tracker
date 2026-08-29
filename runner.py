#!/usr/bin/env python3
"""
Multi-domain engineering task orchestrator.
Executes distinct tasks depending on the scheduled run:
1. Algorithm & Data Structure verification
2. RAG latency & precision benchmarking
3. arXiv CS research indexing
4. Model architecture metrics
5. Code health & system audits
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

from benchmarks.rag_eval import run_retrieval_benchmark
from challenges.solutions import max_subarray_sum, merge_k_sorted_lists
from tracker import run as run_arxiv_tracker


def run_benchmark_task():
    print("[Task] Running RAG retrieval latency benchmark...")
    res = run_retrieval_benchmark()
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    
    os.makedirs("data/benchmarks", exist_ok=True)
    os.makedirs("reports/benchmarks", exist_ok=True)
    
    out_file = f"data/benchmarks/rag_perf_{date_str}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"timestamp": now_utc.isoformat(), "metrics": res}, f, indent=2)
        
    report_file = f"reports/benchmarks/rag_eval_{date_str}.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"# RAG Retrieval Latency & Hit Rate Benchmark ({date_str})\n\n")
        f.write(f"- Average Latency: `{res['avg_latency_ms']} ms`\n")
        f.write(f"- P95 Latency: `{res['p95_latency_ms']} ms`\n")
        f.write(f"- Hit Rate: `{res['hit_rate_pct']}%`\n")
        f.write(f"- Documents Ingested: `{res['num_docs']}`\n")
    print(f"[+] Saved benchmark results to {out_file} and {report_file}")


def run_algorithms_task():
    print("[Task] Running algorithmic challenge test suite...")
    assert max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert merge_k_sorted_lists([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    
    now_utc = datetime.now(timezone.utc)
    date_str = now_utc.strftime("%Y-%m-%d")
    os.makedirs("data/leetcode", exist_ok=True)
    
    with open(f"data/leetcode/status_{date_str}.json", "w", encoding="utf-8") as f:
        json.dump({"verified_at": now_utc.isoformat(), "status": "all_passed", "suites": ["kadane", "min_heap_k_way_merge"]}, f, indent=2)
    print("[+] Algorithm test suite passed.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", choices=["arxiv", "benchmark", "algorithms", "all"], default="all")
    args = parser.parse_args()
    
    if args.task in ["arxiv", "all"]:
        run_arxiv_tracker()
    if args.task in ["benchmark", "all"]:
        run_benchmark_task()
    if args.task in ["algorithms", "all"]:
        run_algorithms_task()


if __name__ == "__main__":
    main()
