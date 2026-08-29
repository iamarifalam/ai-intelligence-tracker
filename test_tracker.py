#!/usr/bin/env python3
"""
Unit tests for tracker pipeline and schema validation.
"""

import unittest
from tracker import build_daily_digest, fetch_arxiv_papers


class TestTracker(unittest.TestCase):
    def test_build_daily_digest(self):
        sample_papers = [
            {
                "title": "Sample Attention Mechanisms",
                "summary": "Evaluation of sparse attention.",
                "published": "2026-08-29",
                "url": "https://arxiv.org/abs/test",
                "authors": ["A. Author", "B. Author"],
            }
        ]
        sample_models = [
            {
                "id": "org/model-7b",
                "likes": 120,
                "downloads": 5400,
                "pipeline_tag": "text-generation",
                "url": "https://huggingface.co/org/model-7b",
            }
        ]
        digest = build_daily_digest(sample_papers, sample_models)
        self.assertIn("Daily Research Summary", digest)
        self.assertIn("Sample Attention Mechanisms", digest)
        self.assertIn("org/model-7b", digest)

    def test_fetch_arxiv_structure(self):
        papers = fetch_arxiv_papers(max_results=1)
        if papers:
            self.assertIn("title", papers[0])
            self.assertIn("url", papers[0])
            self.assertIn("authors", papers[0])


if __name__ == "__main__":
    unittest.main()
