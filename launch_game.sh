#!/bin/bash
# Termux:Widget launcher script for The Hancox Wedding Sweepstake
# Place this file in ~/.shortcuts/ on the tablet
#
# Prerequisites:
# 1. Install Termux from F-Droid
# 2. Install Termux:Widget from F-Droid
# 3. Run: mkdir -p ~/.shortcuts && cp launch_game.sh ~/.shortcuts/
# 4. Run: chmod +x ~/.shortcuts/launch_game.sh
# 5. Add a Termux:Widget widget to the home screen
# 6. Tap the shortcut to launch
#
# This script starts the Flask server and opens Chrome in fullscreen (kiosk) mode.

# Path to the game directory — update this to match your tablet
GAME_DIR="$HOME/Game"

# Kill any existing Flask server on port 5000
pkill -f "python app.py" 2>/dev/null
sleep 1

# Start the Flask server in the background
cd "$GAME_DIR" || exit 1
nohup python app.py > /dev/null 2>&1 &

# Wait for the server to start
sleep 3

# Open Chrome in fullscreen/kiosk-like mode
am start -a android.intent.action.VIEW \
    -d "http://127.0.0.1:5000" \
    -n com.android.chrome/com.google.android.apps.chrome.Main \
    --ez create_new_tab true 2>/dev/null

# Alternative: if the above doesn't work, try generic browser intent
# am start -a android.intent.action.VIEW -d "http://127.0.0.1:5000"
