# AI Intelligence & Research Tracker 🧠⚡

An automated, open-source intelligence pipeline that tracks, analyzes, and synthesizes daily breakthroughs in Artificial Intelligence, Large Language Models (LLMs), and Machine Learning architectures.

[![Daily AI Research & Model Intelligence](https://github.com/iamarifalam/ai-intelligence-tracker/actions/workflows/daily_intelligence.yml/badge.svg)](https://github.com/iamarifalam/ai-intelligence-tracker/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🌟 What This Project Does

- 🔬 **arXiv AI Monitor**: Crawls and parses cutting-edge papers daily across `cs.AI` (Artificial Intelligence), `cs.CL` (Computation & Language), and `cs.LG` (Machine Learning).
- 🚀 **Hugging Face Model Indexer**: Tracks weekly trending open-weights models, architectures, and community adoption metrics.
- 📊 **Structured Datasets**: Emits structured daily JSON records in [`data/daily/`](./data/daily/) for downstream analysis, data pipelines, and research benchmarks.
- 📝 **Automated Digest Reports**: Compiles human-readable daily synthesis reports into [`reports/`](./reports/) and keeps [`reports/LATEST.md`](./reports/LATEST.md) updated.

---

## 📂 Repository Architecture

```text
├── data/
│   └── daily/                  # Daily structured JSON intelligence datasets
│       └── ai_intel_YYYY-MM-DD.json
├── reports/
│   ├── LATEST.md               # Most recent intelligence summary
│   └── report_YYYY-MM-DD.md    # Historical daily archives
├── tracker.py                  # Core intelligence crawler & synthesizer
├── test_tracker.py             # Unit test suite verifying schema and integrity
└── .github/
    └── workflows/
        └── daily_intelligence.yml  # Automated CI/CD scheduled pipeline
```

---

## 🛠️ Local Development & Testing

### 1. Run Intelligence Pipeline
```bash
python3 tracker.py
```

### 2. Run Test Suite
```bash
python3 -m unittest test_tracker.py
```

---

## 📜 Automated CI/CD Execution
The workflow runs automatically via **GitHub Actions** on a 12-hour cron schedule (`04:00` and `16:00` UTC) with full validation tests before committing changes.

## 📄 License
MIT © [Arif Alam](https://github.com/iamarifalam)
