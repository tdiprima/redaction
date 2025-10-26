"""
PII redaction script using Microsoft Presidio.
Processes a file line by line and creates an output file with redacted content.
"""

import argparse
import sys
from pathlib import Path

# Import Presidio
try:
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
except ImportError:
    print("Please install presidio: pip install presidio-analyzer presidio-anonymizer")
    sys.exit(1)

# Import rich_argparse for better CLI output
try:
    from rich_argparse import RichHelpFormatter
except ImportError:
    print("Please install rich_argparse: pip install rich-argparse")
    RichHelpFormatter = argparse.RawDescriptionHelpFormatter


class PresidioRedactor:
    """Handles PII redaction using Microsoft Presidio."""

    def __init__(self):
        """Initialize Presidio engines."""
        self.presidio_analyzer = AnalyzerEngine()
        self.presidio_anonymizer = AnonymizerEngine()

    def redact(self, text):
        """Redact PII using Microsoft Presidio."""
        # Analyze the text for PII
        results = self.presidio_analyzer.analyze(text=text, language="en")

        # Anonymize the detected PII if any found
        if results:
            anonymized = self.presidio_anonymizer.anonymize(
                text=text, analyzer_results=results
            )
            return anonymized.text
        return text

    def process_file(self, input_file, output_file=None):
        """Process a file line by line using Presidio."""
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"Error: Input file '{input_file}' not found.")
            return False

        # Determine output file name
        output_path = Path(output_file or f"{input_path.stem}_redacted.txt")

        print(f"Processing file: {input_path}")
        print(f"Output file: {output_path}\n")

        # Process the file
        with open(input_path, "r", encoding="utf-8") as infile, \
             open(output_path, "w", encoding="utf-8") as outfile:

            line_count = 0
            for line_num, line in enumerate(infile, 1):
                line_content = line.rstrip("\n")

                # Handle empty lines
                if not line_content:
                    outfile.write("\n")
                    continue

                line_count += 1

                # Apply Presidio redaction and write output
                outfile.write(self.redact(line_content) + "\n")

                # Progress indicator for large files
                if line_num % 100 == 0:
                    print(f"  Processed {line_num} lines...")

            print(f"\nSuccessfully processed {line_count} non-empty lines.")
            return True


def main():
    """Main function to handle command-line arguments and run the redactor."""
    parser = argparse.ArgumentParser(
        description="Redact PII from text files using Microsoft Presidio.",
        formatter_class=RichHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.txt
  %(prog)s input.txt -o cleaned.txt
  %(prog)s sensitive_data.txt -o /path/to/output/safe_data.txt

The script uses Microsoft Presidio to detect and redact PII.
        """,
    )

    parser.add_argument("input_file", help="Path to the input file to be redacted")
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Output file name (default: input_filename_redacted.txt)",
    )

    args = parser.parse_args()

    # Initialize the redactor and process the file
    print("Initializing Presidio...\n")
    redactor = PresidioRedactor()

    if redactor.process_file(args.input_file, args.output_file):
        print("\nRedaction complete!")
        print("Note: Always manually review the output file to ensure all sensitive data has been properly redacted.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
