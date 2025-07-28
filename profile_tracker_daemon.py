#!/usr/bin/env python3
import subprocess
import time
import psutil
from pathlib import Path
import configparser

# Snap profile location
FIREFOX_PROFILES_DIR = Path.home() / "snap/firefox/common/.mozilla/firefox"
FIREFOX_PROFILES_INI = FIREFOX_PROFILES_DIR / "profiles.ini"
PROFILE_TRACKER = Path(__file__).parent / "profile_tracker.txt"

def parse_profiles_ini():
    parser = configparser.RawConfigParser()
    parser.read(FIREFOX_PROFILES_INI)

    profile_map = {}
    for section in parser.sections():
        if section.startswith("Profile"):
            name = parser.get(section, "Name")
            path = parser.get(section, "Path")
            abs_path = FIREFOX_PROFILES_DIR / path
            profile_map[abs_path.resolve()] = name
    return profile_map

def get_focused_window_pid():
    try:
        pid = subprocess.check_output(["xdotool", "getwindowfocus", "getwindowpid"]).decode().strip()
        return int(pid)
    except Exception:
        return None

def is_firefox_window(pid):
    try:
        proc = psutil.Process(pid)
        name = proc.name().lower()
        exe = proc.exe().lower()
        return "firefox" in name or "firefox" in exe
    except Exception:
        return False

def get_profile_name_from_pid(pid, profile_map):
    try:
        proc = psutil.Process(pid)
        open_files = proc.open_files()
        for f in open_files:
            for profile_path, profile_name in profile_map.items():
                if f.path.startswith(str(profile_path)) and ".parentlock" in f.path:
                    return profile_name
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return None

def track_active_profile():
    last_profile = None
    profile_map = parse_profiles_ini()

    while True:
        pid = get_focused_window_pid()
        if pid and is_firefox_window(pid):
            profile_name = get_profile_name_from_pid(pid, profile_map)
            if profile_name and profile_name != last_profile:
                PROFILE_TRACKER.write_text(profile_name)
                print(f"[INFO] Focused Firefox window using profile: {profile_name}")
                last_profile = profile_name
        time.sleep(1)

if __name__ == "__main__":
    track_active_profile()