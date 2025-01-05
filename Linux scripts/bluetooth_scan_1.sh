#!/bin/bash

# Trap SIGINT (Ctrl+C) to stop the script
trap "echo -e '\nStopping scan...'; sudo hcitool noscan; exit 0" SIGINT

echo "Starting detailed Bluetooth scan..."
echo "Press Ctrl+C to stop."

# Start btmon in the background to monitor advertising packets
sudo btmon > /tmp/btmon_log &
BTMON_PID=$!

# Run hcitool to start scanning
sudo hcitool lescan --duplicates > /tmp/scan_log &
HCITOOL_PID=$!

# Display results in real-time
tail -f /tmp/scan_log &

# Wait for Ctrl+C to stop the processes
wait