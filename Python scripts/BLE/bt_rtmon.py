import asyncio;
from bleak import BleakScanner

async def monitor_ble_devices():
    def detection_callback(device, advertisement_data):
        print(f"Device found: {device.name} - {device.address}")
        print(f"  RSSI: {device.rssi}")
        print(f"  Advertisement Data: {advertisement_data}")

    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()
    await asyncio.sleep(30)  # Scan for 30 seconds
    await scanner.stop()

asyncio.run(monitor_ble_devices())