#!/usr/bin/env python3
"""
Multi-library PII redaction script using scrubadub, presidio, and pii-codex.
Processes a file line by line and creates a single output file with all libraries applied.
"""

import argparse
import sys
from pathlib import Path

# Import the redaction libraries
try:
    import scrubadub
except ImportError:
    print("Please install scrubadub: pip install scrubadub")
    sys.exit(1)

try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
except ImportError:
    print("Please install presidio: pip install presidio-analyzer presidio-anonymizer")
    sys.exit(1)

try:
    from pii_codex import PIIProcessor
except ImportError:
    print("Please install pii-codex: pip install pii-codex")
    sys.exit(1)


class MultiRedactor:
    """Handles redaction using multiple libraries."""

    def __init__(self):
        # Initialize scrubadub (no setup needed)
        self.scrubadub_ready = True

        # Initialize presidio
        try:
            self.presidio_analyzer = AnalyzerEngine()
            self.presidio_anonymizer = AnonymizerEngine()
            self.presidio_ready = True
        except Exception as e:
            print(f"Warning: Presidio initialization failed: {e}")
            self.presidio_ready = False

        # Initialize pii-codex
        try:
            self.pii_processor = PIIProcessor()
            self.pii_codex_ready = True
        except Exception as e:
            print(f"Warning: PII-Codex initialization failed: {e}")
            self.pii_codex_ready = False

    def redact_with_scrubadub(self, text):
        """Redact using scrubadub library."""
        try:
            return scrubadub.clean(text)
        except Exception as e:
            return f"[SCRUBADUB ERROR: {e}] {text}"

    def redact_with_presidio(self, text):
        """Redact using Microsoft Presidio library."""
        if not self.presidio_ready:
            return f"[PRESIDIO NOT AVAILABLE] {text}"

        try:
            # Analyze the text for PII
            results = self.presidio_analyzer.analyze(text=text, language="en")

            # Anonymize the detected PII
            if results:
                anonymized = self.presidio_anonymizer.anonymize(
                    text=text, analyzer_results=results
                )
                return anonymized.text
            return text
        except Exception as e:
            return f"[PRESIDIO ERROR: {e}] {text}"

    def redact_with_pii_codex(self, text):
        """Redact using pii-codex library."""
        if not self.pii_codex_ready:
            return f"[PII-CODEX NOT AVAILABLE] {text}"

        try:
            # Process the text
            result = self.pii_processor.redact(text)
            return result
        except Exception as e:
            return f"[PII-CODEX ERROR: {e}] {text}"

    def process_file(self, input_file, output_file=None):
        """Process a file line by line with all three libraries."""

        input_path = Path(input_file)
        if not input_path.exists():
            print(f"Error: Input file '{input_file}' not found.")
            return False

        # Determine output file name
        if output_file is None:
            output_file = input_path.stem + "_redacted.txt"

        output_path = Path(output_file)

        print(f"Processing file: {input_path}")
        print(f"Output file: {output_path}")
        print()

        # Process the file
        try:
            with (
                open(input_path, "r", encoding="utf-8") as infile,
                open(output_path, "w", encoding="utf-8") as outfile,
            ):

                line_count = 0
                for line_num, line in enumerate(infile, 1):
                    # Remove trailing newline for processing
                    line_content = line.rstrip("\n")

                    # Skip empty lines
                    if not line_content:
                        outfile.write("\n")
                        continue

                    line_count += 1

                    # Apply all libraries sequentially
                    redacted = line_content
                    redacted = self.redact_with_scrubadub(redacted)
                    redacted = self.redact_with_presidio(redacted)
                    redacted = self.redact_with_pii_codex(redacted)

                    # Write output
                    outfile.write(redacted + "\n")

                    # Progress indicator for large files
                    if line_num % 100 == 0:
                        print(f"  Processed {line_num} lines...")

                print(f"\nSuccessfully processed {line_count} non-empty lines.")
                return True

        except Exception as e:
            print(f"Error processing file: {e}")
            return False


def main():
    """Main function to handle command-line arguments and run the redactor."""

    parser = argparse.ArgumentParser(
        description="Redact PII from text files using multiple libraries.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.txt
  %(prog)s input.txt -o cleaned.txt
  %(prog)s sensitive_data.txt -o /path/to/output/safe_data.txt
  
The script applies all three libraries (scrubadub, Presidio, pii-codex) sequentially.
        """,
    )

    parser.add_argument("input_file", help="Path to the input file to be redacted")

    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Output file name (default: input_filename_redacted.txt)",
        default=None,
    )

    args = parser.parse_args()

    # Initialize the redactor
    print("Initializing redaction libraries...")
    redactor = MultiRedactor()
    print()

    # Process the file
    success = redactor.process_file(args.input_file, args.output_file)

    if success:
        print("\nRedaction complete!")
        print(
            "Note: Always manually review the output file to ensure all sensitive data has been properly redacted."
        )
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
