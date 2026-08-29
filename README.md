# AI Intelligence Tracker

A lightweight automated utility that indexes daily research papers from arXiv (`cs.AI`, `cs.CL`, `cs.LG`) and monitors trending models from Hugging Face.

## Overview
- **Data Collection**: Fetches daily paper abstracts and model metadata.
- **Structured Storage**: Saves daily snapshots as JSON in `data/daily/`.
- **Reports**: Generates markdown summaries in `reports/`.

## Usage
```bash
python tracker.py
python -m unittest test_tracker.py
```

## Structure
- `tracker.py` — Main data fetcher and synthesizer
- `test_tracker.py` — Schema validation tests
- `data/` — Daily dataset records
- `reports/` — Daily digest files
