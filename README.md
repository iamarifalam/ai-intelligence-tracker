# ai-engineering-workspace

A continuous engineering toolkit and benchmarking suite covering RAG evaluation, algorithmic challenges, and machine learning research tracking.

## Components

- **RAG Benchmarking (`benchmarks/`)**: Evaluates retrieval latency, hit-rate, and precision across chunk configurations.
- **Algorithms (`challenges/`)**: Implementations and unit test suites for data structures and algorithmic patterns.
- **Research Ingestion (`tracker.py`)**: Data pipeline tracking arXiv machine learning categories and Hugging Face model metadata.
- **Orchestration (`runner.py`)**: Unified execution harness for running individual or matrix workloads.

## Getting Started

### Prerequisites
- Python 3.10+

### Installation
```bash
git clone https://github.com/iamarifalam/ai-intelligence-tracker.git
cd ai-intelligence-tracker
```

### Running Tasks
```bash
# Run all components
python runner.py --task all

# Run individual benchmarks
python runner.py --task benchmark
python runner.py --task algorithms
python runner.py --task arxiv
```

### Running Tests
```bash
python -m unittest discover -s .
```

## License
MIT
