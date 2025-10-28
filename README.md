# 🕵️ PII Redaction Tool

A no-nonsense (but kinda cool) script that wipes out personal info from text files using **Microsoft Presidio**.

Does not require Torch.

Tried **scrubadub** and **pii-codex**, but they didn't quite pass the vibe check — so this one gets the job done.

## 🚀 Usage

```bash
pip install redaction

redact file.txt
redact file.txt -o output.txt
redact --help
```

* By default, the redacted version lands in the same directory as your input file.
* Use the `-o` flag to specify your own output file.
