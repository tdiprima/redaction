from redaction.cli import redact_vast_tokens

SECRET = "AbC123.dEf-456_ghi+/="


def test_labelled_tokens_redacted():
    for line in (
        f"VMS API Token: {SECRET}",
        f"vms api token : {SECRET}",
        f"VAST API Token = {SECRET}",
        f"VAST_API_TOKEN={SECRET}",
        f'"vms_token": "{SECRET}",',
        f"Authorization: Api-Token {SECRET}",
    ):
        out = redact_vast_tokens(line)
        assert SECRET not in out, line
        assert "<VAST_API_TOKEN>" in out, line


def test_label_kept_and_other_text_untouched():
    assert redact_vast_tokens(f"VMS API Token: {SECRET}") == "VMS API Token: <VAST_API_TOKEN>"
    for line in ("The VMS token expired yesterday.", "vast cluster: prod-01", "token=abc123"):
        assert redact_vast_tokens(line) == line
