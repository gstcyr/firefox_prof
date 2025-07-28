# Firefox Prof: Smart Firefox Profile URL Handler

Firefox Prof (`firefox_prof`) is a small utility that makes **Firefox behave like Chrome** when it comes to profiles. It tracks which Firefox profile was last active, and ensures that URLs opened from external apps (like Slack, Thunderbird, or Terminal) are opened in the correct Firefox window.

---

## 🚀 Features

- 📌 Remembers the **last active Firefox profile** based on focused window
- 🌐 Opens external URLs (via `xdg-open`, email, Slack, etc.) in the correct profile
- 🖥️ Runs as a background service using `systemd --user`
- ✅ Works with Snap-based Firefox installs
- 🔒 Uses a Python virtual environment to keep dependencies isolated

---

## 🛠️ Installation Instructions

For quick install, use the `setup.sh` script:

```bash
chmod +x setup.sh
./setup.sh
```


### 🐧 Install Dependencies

Make sure these are installed:

```bash
sudo apt install xdotool
```

### 1. Clone and Set Up

```bash
git clone https://github.com/gstcyr/firefox_prof
cd firefox_prof
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install psutil
```

### 3. Register the URL Handler

Create the desktop file:

```bash
mkdir -p ~/.local/share/applications
nano ~/.local/share/applications/firefox-url-handler.desktop
```

Paste the following (adjust paths):

```ini
[Desktop Entry]
Name=Firefox Profile URL Launcher
Exec=/full/path/to/firefox_prof/venv/bin/python3 /full/path/to/firefox_prof/firefox_url_launcher.py %u
Type=Application
Terminal=false
MimeType=x-scheme-handler/http;x-scheme-handler/https;
```

Register it:

```bash
xdg-mime default firefox-url-handler.desktop x-scheme-handler/http
xdg-mime default firefox-url-handler.desktop x-scheme-handler/https
```

---

## ⚙️ Enable the Tracker Daemon

### 1. Create the systemd service

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/firefox-profile-tracker.service
```

Paste this (update path as needed):

```ini
[Unit]
Description=Firefox Profile Tracker Daemon
After=default.target

[Service]
ExecStart=/full/path/to/firefox_prof/venv/bin/python3 /full/path/to/firefox_prof/profile_tracker_daemon.py
Restart=on-failure

[Install]
WantedBy=default.target
```

### 2. Enable and start the service

```bash
systemctl --user daemon-reexec
systemctl --user enable firefox-profile-tracker.service
systemctl --user start firefox-profile-tracker.service
```

Check logs:
```bash
systemctl --user status firefox-profile-tracker.service
```

### 3. Test:

```bash
xdg-open https://example.com
```

---

## 🧪 How It Works

- `profile_tracker_daemon.py` runs in the background.
- It uses `xdotool` and `psutil` to detect the currently focused Firefox window.
- It extracts the active profile by matching `.parentlock` files with Firefox PIDs.
- The launcher script (`firefox_url_launcher.py`) reads this profile and opens the incoming URL in the right Firefox process.

---


---

## 🧹 Optional Cleanup

If you see GTK warnings like:

```
Gtk-Message: Failed to load module "canberra-gtk-module"
```

You can suppress them by editing `firefox_url_launcher.py`:

```python
subprocess.Popen([...], stderr=subprocess.DEVNULL)
```

---

## 🙌 Credits

Created by Gilles St-Cyr and ChatGPT. Inspired by Chrome’s smarter profile handling.

---