#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

FIREFOX_PATH = "/usr/bin/firefox"  # Adjust if needed
PROFILE_TRACKER = Path(__file__).parent / "profile_tracker.txt"

def get_last_used_profile():
    if PROFILE_TRACKER.exists():
        return PROFILE_TRACKER.read_text().strip()
    return None

def open_url_with_profile(url: str, profile_name: str):
    subprocess.Popen([
        FIREFOX_PATH,
        "-P", profile_name,
        "-no-remote",
        "-new-tab", url
    ])

def main():
    if len(sys.argv) < 2:
        print("Expected a URL argument")
        return

    url = sys.argv[1]
    profile = get_last_used_profile()
    if not profile:
        print("No active profile. Set it in profile_tracker.txt")
        return

    open_url_with_profile(url, profile)

if __name__ == "__main__":
    main()
