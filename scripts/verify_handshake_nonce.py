#!/usr/bin/env python3
"""
Handshake Nonce Verification Script

This script verifies the HANDSHAKE_NONCE value from GitHub Actions workflow logs.
It extracts the nonce from a specific workflow run and validates its format.
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime

def run_gh_command(args):
    """Run gh CLI command and return output."""
    try:
        result = subprocess.run(["gh"] + args, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running gh command: {e}")
        print(f"stderr: {e.stderr}")
        return None

def get_workflow_log(run_id):
    """Get workflow log for a given run ID."""
    cmd = ["run", "view", str(run_id), "--repo", "ai-village-agents/ai-village-agent-bridge", "--log"]
    return run_gh_command(cmd)

def extract_nonce_from_log(log_text):
    """Extract HANDSHAKE_NONCE value from workflow log."""
    # Pattern 1: HANDSHAKE_NONCE=value (in echo command)
    pattern1 = r'HANDSHAKE_NONCE=(\d+)'
    # Pattern 2: HANDSHAKE_NONCE: value (in environment section)
    pattern2 = r'HANDSHAKE_NONCE:\s*(\d+)'
    
    # Try pattern 2 first (more likely in log)
    match = re.search(pattern2, log_text)
    if match:
        return match.group(1)
    
    # Try pattern 1
    match = re.search(pattern1, log_text)
    if match:
        return match.group(1)
    
    # Fallback: look for 19-digit number after HANDSHAKE_NONCE
    lines = log_text.split('\n')
    for line in lines:
        if 'HANDSHAKE_NONCE' in line:
            # Find all numbers in the line
            numbers = re.findall(r'\d{19}', line)
            if numbers:
                return numbers[0]
    
    return None

def validate_nonce_format(nonce):
    """Validate nonce format: 19 digits = seconds (10) + nanoseconds (9)."""
    if not nonce or not nonce.isdigit():
        return False, "Nonce must be all digits"
    
    if len(nonce) != 19:
        return False, f"Nonce should be 19 digits (seconds+nanoseconds), got {len(nonce)}"
    
    seconds = int(nonce[:10])
    nanoseconds = int(nonce[10:])
    
    # Check if seconds is reasonable (after 2020)
    if seconds < 1577836800:  # 2020-01-01
        return False, f"Seconds part {seconds} seems too old"
    
    # Nanoseconds should be < 1e9
    if nanoseconds >= 1000000000:
        return False, f"Nanoseconds part {nanoseconds} should be < 1,000,000,000"
    
    # Convert to human readable
    dt = datetime.fromtimestamp(seconds)
    return True, f"Valid nonce: timestamp={dt.isoformat()}, nanoseconds={nanoseconds:09d}"

def verify_specific_run(run_id, expected_nonce=None):
    """Verify nonce for a specific workflow run."""
    print(f"\n--- Verifying Run ID: {run_id} ---")
    
    # Step 1: Get workflow log
    print("1. Fetching workflow log...")
    log_text = get_workflow_log(run_id)
    
    if not log_text:
        print("   ERROR: Failed to fetch workflow log")
        return None, False
    
    print(f"   Log retrieved ({len(log_text)} characters)")
    
    # Step 2: Extract nonce
    print("2. Extracting nonce from log...")
    extracted_nonce = extract_nonce_from_log(log_text)
    
    if not extracted_nonce:
        print("   ERROR: Could not extract HANDSHAKE_NONCE from log")
        # Save log snippet for debugging
        snippet = log_text[:2000]
        with open(f"/tmp/run_{run_id}_log_snippet.txt", "w") as f:
            f.write(snippet)
        print(f"   Saved log snippet to /tmp/run_{run_id}_log_snippet.txt")
        return None, False
    
    print(f"   Extracted nonce: {extracted_nonce}")
    
    # Step 3: Validate format
    print("3. Validating nonce format...")
    is_valid, message = validate_nonce_format(extracted_nonce)
    print(f"   {message}")
    
    # Step 4: Compare with expected if provided
    if expected_nonce:
        print("4. Comparing with expected nonce...")
        if extracted_nonce == expected_nonce:
            print(f"   SUCCESS: Nonce matches expected value")
            match = True
        else:
            print(f"   MISMATCH: '{extracted_nonce}' != '{expected_nonce}'")
            match = False
    else:
        match = None
    
    return extracted_nonce, is_valid and (match if expected_nonce else True)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Verify handshake nonce from GitHub Actions workflow")
    parser.add_argument("--run-id", type=int, default=23866620093, help="Workflow run ID to verify")
    parser.add_argument("--expected", type=str, help="Expected nonce value (optional)")
    parser.add_argument("--list-runs", action="store_true", help="List recent workflow runs")
    args = parser.parse_args()
    
    print("=== Handshake Nonce Verification Tool ===\n")
    
    # List recent runs if requested
    if args.list_runs:
        print("Listing recent workflow runs...")
        cmd = ["run", "list", "--repo", "ai-village-agents/ai-village-agent-bridge", "--limit", "5", "--json", "number,displayTitle,workflowName,createdAt,conclusion"]
        output = run_gh_command(cmd)
        if output:
            runs = json.loads(output)
            for run in runs:
                print(f"  #{run['number']}: {run['workflowName']} - {run['displayTitle']} ({run['createdAt']}) - {run.get('conclusion', 'pending')}")
        print()
        return
    
    # Verify specific run
    expected = args.expected or ("1775071409503051311" if args.run_id == 23866620093 else None)
    
    nonce, success = verify_specific_run(args.run_id, expected)
    
    # Generate verification report
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "run_id": args.run_id,
        "extracted_nonce": nonce,
        "expected_nonce": expected,
        "verification_success": success,
        "verification_steps": {
            "log_retrieved": nonce is not None,
            "nonce_extracted": nonce is not None,
            "format_validated": success if nonce else False,
            "match_verified": nonce == expected if expected else None
        }
    }
    
    # Save report
    report_file = f"/tmp/handshake_nonce_verification_{args.run_id}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nVerification report saved to {report_file}")
    
    # Overall status
    if success:
        print("\n✅ VERIFICATION SUCCESSFUL")
        return 0
    else:
        print("\n⚠️  VERIFICATION FAILED OR INCOMPLETE")
        return 1

if __name__ == "__main__":
    sys.exit(main())
