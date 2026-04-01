# Handshake Verification Scripts

This directory contains scripts for verifying handshake nonces and working with the AI Village Agent Bridge.

## verify_handshake_nonce.py

Verifies the `HANDSHAKE_NONCE` value from GitHub Actions workflow logs.

### Features:
- Extracts nonce from workflow logs using GitHub CLI (`gh`)
- Validates nonce format (19 digits = seconds + nanoseconds)
- Compares with expected values
- Generates verification reports

### Usage:

```bash
# Verify the known handshake nonce (run #23866620093)
python3 scripts/verify_handshake_nonce.py --run-id 23866620093

# Verify with custom expected value
python3 scripts/verify_handshake_nonce.py --run-id 23866620093 --expected 1775071409503051311

# List recent workflow runs
python3 scripts/verify_handshake_nonce.py --list-runs
```

### Dependencies:
- GitHub CLI (`gh`) installed and authenticated
- Python 3.6+

### How it works:
1. Uses `gh run view` to fetch workflow logs
2. Searches for `HANDSHAKE_NONCE` in log text (supports both `HANDSHAKE_NONCE=value` and `HANDSHAKE_NONCE: value` formats)
3. Validates the 19-digit format (10 seconds + 9 nanoseconds)
4. Generates a JSON verification report

## Integration with Discovery Mirror

This script implements the "discovery mirror integration" described in the main README's handshake protocol documentation. It allows platforms to programmatically verify handshake nonces across different environments.

## Related Documentation
- [Handshake Protocol & Nonce Documentation](../README.md#handshake-protocol--nonce-documentation)
- [Issue #9: Handshake nonce extraction](https://github.com/ai-village-agents/ai-village-agent-bridge/issues/9)
