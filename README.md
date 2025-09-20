# PII Redaction Tool

Multi-library PII redaction script that processes text files using scrubadub, Microsoft Presidio, and pii-codex libraries.

## Usage

```bash
python main.py input.txt
python main.py input.txt -o output.txt
```

## Installation

```bash
uv sync
```

Or with pip:
```bash
pip install -e .
```

Creates a single output file with all three libraries applied sequentially.
