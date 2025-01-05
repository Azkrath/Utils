#!/bin/bash

# Function to scan and display devices
scan_bluetooth() {
    echo "Scanning for Bluetooth devices..."
    bluetoothctl scan on > /tmp/scan_results &
    SCAN_PID=$!
    sleep 5
    kill $SCAN_PID

    DEVICES=$(bluetoothctl devices | awk '{print $2 " " $3}')
    echo "Devices Found:"
    echo "$DEVICES"
}

# Main Menu Loop
while true; do
    CHOICE=$(whiptail --title "Bluetooth Console App" --menu "Choose an option" 15 50 4 \
        "1" "Scan for devices" \
        "2" "Exit" 3>&1 1>&2 2>&3)

    case $CHOICE in
        1) scan_bluetooth ;;
        2) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid choice";;
    esac
done