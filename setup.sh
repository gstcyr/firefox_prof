#!/bin/bash

set -e
REPO_DIR="$(cd "$(dirname "$0")"; pwd)"
VENV_DIR="$REPO_DIR/venv"
DESKTOP_FILE="$HOME/.local/share/applications/firefox-url-handler.desktop"
SERVICE_FILE="$HOME/.config/systemd/user/firefox-profile-tracker.service"

echo "🔧 Installing required system packages..."
if ! command -v xdotool >/dev/null 2>&1; then
    sudo apt update
    sudo apt install -y xdotool
fi

echo "🔧 Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"

echo "📦 Installing Python dependencies..."
"$VENV_DIR/bin/pip" install --upgrade pip psutil

echo "📝 Creating .desktop file..."
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=Firefox Profile URL Launcher
Exec=$VENV_DIR/bin/python3 $REPO_DIR/firefox_url_launcher.py %u
Type=Application
Terminal=false
MimeType=x-scheme-handler/http;x-scheme-handler/https;
EOF

echo "🔗 Registering URL handler..."
xdg-mime default firefox-url-handler.desktop x-scheme-handler/http
xdg-mime default firefox-url-handler.desktop x-scheme-handler/https

echo "🛠️ Creating systemd user service..."
mkdir -p "$(dirname "$SERVICE_FILE")"
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Firefox Profile Tracker Daemon
After=default.target

[Service]
ExecStart=$VENV_DIR/bin/python3 $REPO_DIR/profile_tracker_daemon.py
Restart=on-failure

[Install]
WantedBy=default.target
EOF

echo "🚀 Enabling and starting service..."
systemctl --user daemon-reexec
systemctl --user enable --now firefox-profile-tracker.service

echo "✅ Setup complete!"
echo "You can test with: xdg-open https://example.com"
