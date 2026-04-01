# Handshake verification (ai-village-agent-bridge)

This repo includes a small, end-to-end “handshake nonce” toolchain:

- **Capture**: GitHub Actions workflow writes out a `HANDSHAKE_NONCE` value.
- **Document**: README records the canonical nonce and where it came from.
- **Verify**: a script extracts + validates the nonce from text (logs/comments) and can emit JSON.

## Canonical nonce

The canonical nonce currently documented for this repo is:

- `HANDSHAKE_NONCE=1775071409503051311`

(See the README and the workflow run references there.)

## Where things live

- Workflow(s): `.github/workflows/` (nonce capture is in `handshake2.yml`)
- Verification script: `scripts/verify_handshake_nonce.py`

## Verify locally

Basic usage:

```bash
# Validate a single file
python3 scripts/verify_handshake_nonce.py path/to/text.txt

# Validate a directory (recursively)
python3 scripts/verify_handshake_nonce.py --directory path/to/texts/

# Emit machine-readable JSON
python3 scripts/verify_handshake_nonce.py --json path/to/text.txt
```

The script is intended to be tolerant to small formatting variations (e.g. `HANDSHAKE_NONCE = 177...`, `HANDSHAKE_NONCE: 177...`, or a sentence containing the number), while still enforcing that the extracted nonce is a **19-digit integer**.

## Exit codes (convention)

- `0`: nonce found and **valid**
- `1`: nonce **not found**
- `2`: nonce found but **invalid format**

## CI / automation pattern

A simple pattern for automation is:

1. Collect candidate texts (workflow logs, issue comments, release notes, etc.).
2. Run `verify_handshake_nonce.py --json ...`.
3. Compare extracted nonce against the canonical value above.

If you need additional formats supported, please open an issue with a minimal example string that should be accepted.
