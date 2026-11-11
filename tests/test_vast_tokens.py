from redaction.cli import redact_vast_tokens

SECRET = "AbC123.dEf-456_ghi+/="
VMS_KEY = "Ab3dEf9h.0123456789abcdefABCDEF0123456789"  # fake, real shape: 8 chars, dot, 32 chars


def test_labelled_tokens_redacted():
    for line in (
        f"VMS API Token: {SECRET}",
        f"vms api token : {SECRET}",
        f"VAST API Token = {SECRET}",
        f"VAST_API_TOKEN={SECRET}",
        f'"vms_token": "{SECRET}",',
        f"Authorization: Api-Token {SECRET}",
        f"VMS API Token: KEEP HIGHLY SECURED!  {SECRET}",
    ):
        out = redact_vast_tokens(line)
        assert SECRET not in out, line
        assert "<VAST_API_TOKEN>" in out, line


def test_vms_key_format_redacted_without_label():
    assert redact_vast_tokens(f"use {VMS_KEY} here") == "use <VAST_API_TOKEN> here"
    assert redact_vast_tokens(f"VMS API Token: KEEP SAFE!  {VMS_KEY}") == "VMS API Token: KEEP SAFE!  <VAST_API_TOKEN>"


def test_label_kept_and_other_text_untouched():
    assert redact_vast_tokens(f"VMS API Token: {SECRET}") == "VMS API Token: <VAST_API_TOKEN>"
    for line in (
        "The VMS token expired yesterday.",
        "vast cluster: prod-01",
        "token=abc123",
        "VAST_VMS_TOKEN: The VMS API token provided separately.",
        'VMS_TOKEN = os.environ["VAST_VMS_TOKEN"]',
        '"Authorization": f"Api-Token {VMS_TOKEN}",',
        "VAST_VMS_TOKEN: ${{ secrets.VAST_VMS_TOKEN }}",
    ):
        assert redact_vast_tokens(line) == line
