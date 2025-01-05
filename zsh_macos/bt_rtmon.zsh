#!/bin/zsh

# Trap SIGINT (Ctrl+C) to stop the script
trap "echo 'Exiting...'; exit 0" SIGINT

echo "Scanning for Bluetooth devices..."
echo "Press Ctrl+C to stop."

while true; do
    # Run AppleScript to get nearby Bluetooth devices
    devices=$(osascript -e '
        tell application "System Events"
            set btDevices to {}
            repeat with d in (get every bluetooth device)
                set deviceName to name of d
                set macAddress to address of d
                set isConnected to connected of d
                set end of btDevices to deviceName & " (" & macAddress & ")" & " - Connected: " & isConnected
            end repeat
            return btDevices
        end tell
    ')

    echo "$devices"
    echo "Scanning again in 5 seconds..."
    sleep 5
done