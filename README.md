# 🕵️ PII Redaction Tool

Wipes out personal info from text files using **[Microsoft Presidio](https://github.com/microsoft/presidio)**.

Built for devs who want something lightweight, fast, and Torch-free — a no-drama way to clean text.

## 🚀 Installation

```bash
pip install redaction
````

## 🧹 Usage

```bash
redact file.txt
redact file.txt -o output.txt
redact --help
```

* By default, the redacted version lands in the same directory as your input file.
* Use the `-o` flag to specify your own output file.

## 💡 Example

**Input:**

```
My name is John Doe and my email is john@example.com.
```

**Output:**

```
My name is <PERSON> and my email is <EMAIL_ADDRESS>.
```

## 🧠 Tech Notes

* Built on top of Microsoft Presidios Analyzer + Anonymizer.
* No GPU, no Torch — just clean text ops.
* Designed for quick local use or integration in your data pipeline.

## ⚙️ License

MIT © 2025

**GitHub:** [https://github.com/tdiprima/redaction](https://github.com/tdiprima/redaction)
