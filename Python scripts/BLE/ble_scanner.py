import asyncio
from bleak import BleakScanner

# Function to parse and display manufacturer data
def parse_manufacturer_data(manufacturer_data):
    for company_id, data in manufacturer_data.items():
        print(f"  Manufacturer ID: {company_id}")
        print(f"  Data (hex): {data.hex()}")
        print(f"  Data (ascii, if readable): {data.decode(errors='ignore')}")

# Function to handle device discovery
def handle_device(device, advertisement_data):
    print(f"Device found: {device.address}")
    print(f"  Name: {device.name or 'Unknown'}")
    print(f"  RSSI: {device.rssi} dBm")

    # Parse Manufacturer Data if available
    if advertisement_data.manufacturer_data:
        print("  Manufacturer Data:")
        parse_manufacturer_data(advertisement_data.manufacturer_data)

    # Display Service UUIDs
    if advertisement_data.service_uuids:
        print(f"  Service UUIDs: {advertisement_data.service_uuids}")

    print("-" * 50)

# Asynchronous BLE scanning function
async def scan_ble_devices():
    print("Scanning for BLE devices... Press Ctrl+C to stop.")
    scanner = BleakScanner()
    scanner.register_detection_callback(handle_device)

    try:
        await scanner.start()
        while True:
            await asyncio.sleep(5)  # Refresh every 5 seconds
    except asyncio.CancelledError:
        await scanner.stop()

# Main entry point
try:
    asyncio.run(scan_ble_devices())
except KeyboardInterrupt:
    print("\nExiting...")