#!/usr/bin/env python3
"""
Unit tests for AI Intelligence & Research Tracker
"""

import os
import json
import unittest
from tracker import build_daily_digest, fetch_arxiv_papers, fetch_huggingface_trending

class TestAITracker(unittest.TestCase):
    def test_build_daily_digest(self):
        sample_papers = [{
            "title": "Test Paper on Transformers",
            "summary": "This is a test abstract.",
            "published": "2026-08-29",
            "url": "http://arxiv.org/abs/test",
            "authors": ["Author One", "Author Two"]
        }]
        sample_models = [{
            "id": "org/test-model-7b",
            "likes": 500,
            "downloads": 10000,
            "pipeline_tag": "text-generation",
            "url": "https://huggingface.co/org/test-model-7b"
        }]
        digest = build_daily_digest(sample_papers, sample_models)
        self.assertIn("Daily AI Intelligence Report", digest)
        self.assertIn("Test Paper on Transformers", digest)
        self.assertIn("org/test-model-7b", digest)

    def test_fetch_arxiv_structure(self):
        papers = fetch_arxiv_papers(max_results=1)
        if papers:
            self.assertIn("title", papers[0])
            self.assertIn("url", papers[0])
            self.assertIn("authors", papers[0])

if __name__ == "__main__":
    unittest.main()
