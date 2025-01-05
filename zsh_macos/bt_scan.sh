#!/bin/zsh

# Trap SIGINT (Ctrl+C) to stop the script
trap "echo 'Exiting...'; exit 0" SIGINT

echo "Scanning for Bluetooth devices..."
echo "Press Ctrl+C to stop."

while true; do
    # Fetch connected and paired Bluetooth devices
    system_profiler SPBluetoothDataType | awk '
    /Device Name|Address|Connected/ {
        if ($0 ~ /Device Name/) {
            device_name = $3
        } else if ($0 ~ /Address/) {
            address = $2
        } else if ($0 ~ /Connected/) {
            connected = $2
            printf "Device Name: %-20s Address: %-17s Connected: %s\n", device_name, address, connected
        }
    }'
    echo "Scanning again in 2 seconds..."
    sleep 2
done