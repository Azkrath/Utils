import asyncio
from bleak import BleakScanner
import time

# Track active devices
active_devices = {}

# Timeout for removing inactive devices (seconds)
DEVICE_TIMEOUT = 10

# Function to handle device detection
def handle_device(device, advertisement_data):
    current_time = time.time()
    active_devices[device.address] = {
        "name": device.name or "Unknown",
        "rssi": device.rssi,
        "last_seen": current_time,
    }

# Function to refresh console-like output
def print_active_devices():
    # Clear the console
    print("\033[H\033[J", end="")
    print("Real-Time BLE Device Scanner")
    print("=" * 40)

    current_time = time.time()
    to_remove = []

    # Print active devices
    for address, info in active_devices.items():
        # Check if the device has timed out
        if current_time - info["last_seen"] > DEVICE_TIMEOUT:
            to_remove.append(address)
            continue

        print(
            f"Device: {address} | Name: {info['name']} | RSSI: {info['rssi']} dBm"
        )

    # Remove timed-out devices
    for address in to_remove:
        del active_devices[address]

    print("=" * 40)
    print("Press Ctrl+C to stop.")

# Asynchronous BLE scanning function
async def scan_ble_devices():
    print("Initializing BLE Scanner...")
    scanner = BleakScanner()
    scanner.register_detection_callback(handle_device)

    await scanner.start()

    try:
        while True:
            print_active_devices()
            await asyncio.sleep(1)  # Refresh every second
    finally:
        await scanner.stop()

# Main entry point
try:
    asyncio.run(scan_ble_devices())
except KeyboardInterrupt:
    print("\nExiting...")