import asyncio
from bleak import BleakScanner

async def scan_bluetooth_devices():
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    if devices:
        print(f"Found {len(devices)} devices:")
        for device in devices:
            print(f"  Device: {device.name}, Address: {device.address}")
    else:
        print("No devices found.")

asyncio.run(scan_bluetooth_devices())