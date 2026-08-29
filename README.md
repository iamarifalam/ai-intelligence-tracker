# ai-intelligence-tracker

Automated pipeline for collecting, parsing, and storing daily machine learning research papers (arXiv cs.AI, cs.CL, cs.LG) and trending model metadata from Hugging Face.

## Architecture

- `tracker.py`: Main ingestion script that queries APIs, parses payloads, and writes formatted outputs.
- `test_tracker.py`: Integration and unit tests covering response parsing and schema validation.
- `data/daily/`: Daily structured JSON datasets.
- `reports/`: Markdown digest summaries.

## Getting Started

### Prerequisites
- Python 3.10 or higher

### Installation
```bash
git clone https://github.com/iamarifalam/ai-intelligence-tracker.git
cd ai-intelligence-tracker
```

### Running Locally
```bash
python3 tracker.py
```

### Running Tests
```bash
python3 -m unittest test_tracker.py
```

## Data Schema

Each daily run outputs a JSON file in `data/daily/` with the following structure:

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "ISO-8601 timestamp",
  "papers_count": 5,
  "models_count": 5,
  "papers": [
    {
      "title": "string",
      "summary": "string",
      "published": "ISO-8601 string",
      "url": "string",
      "authors": ["string"]
    }
  ],
  "models": [
    {
      "id": "string",
      "likes": 0,
      "downloads": 0,
      "pipeline_tag": "string",
      "url": "string"
    }
  ]
}
```

## License
MIT
