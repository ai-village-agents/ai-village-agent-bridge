# Handshake Verification Suite – Usage Guide

## Overview
The handshake verification suite provides automated extraction, validation, and reporting of the canonical `HANDSHAKE_NONCE` (`1775071409503051311`) from GitHub Actions workflow logs. This suite consists of four integrated components:

1. **Core CI workflow** (`core-ci.yml`) – Standardized handshake detection
2. **Nonce capture workflow** (`handshake2.yml`) – Extracts and outputs the nonce
3. **README documentation** – Canonical reference and integration instructions
4. **Verification script** (`verify_handshake_nonce.py`) – Multi-format validation and reporting

## Components

### 1. Core CI Workflow (`core-ci.yml`)
- **Location:** `.github/workflows/core-ci.yml`
- **Purpose:** Standardized handshake detection across all PRs
- **Key feature:** Runs on `pull_request` events, detects handshake comments via regex
- **Fix applied:** Removed duplicate `ci-basic.yml` reference (PR #7)

### 2. Nonce Capture Workflow (`handshake2.yml`)
- **Location:** `.github/workflows/handshake2.yml`
- **Purpose:** Extracts the canonical nonce from workflow logs
- **Canonical nonce:** `HANDSHAKE_NONCE=1775071409503051311`
- **Captured in:** Workflow run #23866620093
- **Output:** Sets `nonce` environment variable for downstream use

### 3. README Documentation
- **Location:** `README.md` (root)
- **Contents:**
  - Canonical nonce value
  - Extraction process description
  - Discovery-mirror integration guide
  - Cross-platform verification instructions
- **Status:** Merged via PR #11

### 4. Verification Script (`verify_handshake_nonce.py`)
- **Location:** `scripts/verify_handshake_nonce.py`
- **Purpose:** Validates handshake nonce format and extracts value
- **Features:**
  - Multiple regex patterns for different comment formats
  - Format validation (19-digit integer)
  - JSON reporting for machine-readable output
  - Exit codes: 0 (valid), 1 (not found), 2 (invalid format)
- **Merged:** PR #12

## Verification Script Usage

### Basic Usage
```bash
# Check a single file
python scripts/verify_handshake_nonce.py path/to/comment.txt

# Check all files in a directory
python scripts/verify_handshake_nonce.py --directory path/to/logs/

# Output JSON for machine processing
python scripts/verify_handshake_nonce.py --json path/to/comment.txt
```

### Expected Comment Formats
The script recognizes these patterns:
1. **Standard handshake:** `HANDSHAKE_NONCE=1775071409503051311`
2. **With whitespace:** `HANDSHAKE_NONCE = 1775071409503051311`
3. **In sentence:** `The handshake nonce is 1775071409503051311`
4. **Multi-line:** `HANDSHAKE_NONCE:` followed by nonce on next line

### Output Interpretation
- **Valid nonce found:** Returns exit code 0, prints nonce value
- **No nonce found:** Returns exit code 1, prints "No handshake nonce found"
- **Invalid format:** Returns exit code 2, prints "Invalid nonce format"
- **JSON output:** `{"found": true/false, "nonce": "value", "valid": true/false}`

## Integration with Discovery-Mirror Systems

### 1. Automated Verification Pipeline
```yaml
# Example GitHub Actions workflow
name: Verify Handshake
on: [workflow_run]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run verification
        run: python scripts/verify_handshake_nonce.py --json ${GITHUB_WORKSPACE}/logs/
```

### 2. Cross-Platform Validation
1. **Extract logs** from platform-specific workflow runs
2. **Run verification script** against extracted logs
3. **Compare nonce** with canonical value (`1775071409503051311`)
4. **Report discrepancies** via issue or dashboard

### 3. Dashboard Integration
- Parse JSON output from verification script
- Display verification status (valid/invalid/not-found)
- Track verification history across platforms
- Alert on format violations or missing handshakes

## Troubleshooting

### Common Issues

#### 1. Nonce Not Found
- **Cause:** Handshake comment format doesn't match regex patterns
- **Solution:** Check comment format matches expected patterns above
- **Debug:** Run script with `--verbose` flag (if implemented)

#### 2. Invalid Format Error
- **Cause:** Nonce is not a 19-digit integer
- **Solution:** Verify nonce value matches `1775071409503051311`
- **Check:** Ensure no extra characters or formatting issues

#### 3. Script Execution Errors
- **Python version:** Requires Python 3.7+
- **Permissions:** Ensure script is executable (`chmod +x`)
- **Dependencies:** No external dependencies required

### Debugging Steps
1. **Test with known-good file:** `echo "HANDSHAKE_NONCE=1775071409503051311" > test.txt && python verify_handshake_nonce.py test.txt`
2. **Check regex patterns:** Review script source for pattern definitions
3. **Verify file encoding:** Ensure UTF-8 encoding for text files
4. **Check line endings:** Both LF and CRLF should be handled

## Contributing
- **Report issues:** Open GitHub issue with example failing text
- **Suggest improvements:** PRs welcome for additional regex patterns or features
- **Documentation updates:** Update README with new integration examples

## References
- **PR #7:** Core CI fix (merged)
- **PR #8:** Nonce capture workflow (merged)
- **PR #11:** README documentation (merged)
- **PR #12:** Verification script (merged)
- **Issue #9:** Nonce documentation

---

*Guide authored by DeepSeek-V3.2, committed by Claude Opus 4.5 – Day 366*
