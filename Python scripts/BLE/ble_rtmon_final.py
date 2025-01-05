from bleak import BleakScanner
import time, os, asyncio, yaml

# Track active devices
active_devices = {}

# Timeout for removing inactive devices (seconds)
DEVICE_TIMEOUT = 10

# Function to load the manufacturer data from a YAML file
def load_company_identifiers(file_name):
    # Get the path of the current script and construct the full path for the YAML file
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
# Function to get manufacturer from the ID using the loaded YAML data
def get_manufacturer_from_id(manufacturer_id, company_identifiers):
    # Find manufacturer by its assigned number (value)
    return next((entry['name'] for entry in company_identifiers if entry['value'] == manufacturer_id), "Unknown Manufacturer")

# Function to handle device detection and update active devices
def handle_device(device, advertisement_data, company_identifiers):
    current_time = time.time()

    # Extract the manufacturer ID from advertisement data, if present
    manufacturer_id = next((manuf_id for manuf_id in advertisement_data.manufacturer_data), None)
    manufacturer = get_manufacturer_from_id(manufacturer_id, company_identifiers) if manufacturer_id else "Unknown"

    # Update or add the device's info in active_devices
    active_devices[device.address] = {
        "name": device.name or "Unknown",
        "manufacturer": manufacturer,
        "rssi": advertisement_data.rssi,
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

    # Print active devices and remove the ones that have timed out
    for address, info in active_devices.items():
        if current_time - info["last_seen"] > DEVICE_TIMEOUT:
            to_remove.append(address)
            continue
        print(f"Device: {address} | Name: {info['name']} | Manufacturer: {info['manufacturer']} | RSSI: {info['rssi']} dBm")

    # Remove timed-out devices from active_devices
    for address in to_remove:
        del active_devices[address]

    print("=" * 40)
    print("Press Ctrl+C to stop.")

# Asynchronous BLE scanning function
async def scan_ble_devices():
    # Load manufacturer data once at the start
    company_identifiers = load_company_identifiers('vendors.yaml')

    print("Initializing BLE Scanner...")
    scanner = BleakScanner()

    # Register the device detection callback directly
    scanner.register_detection_callback(lambda device, advertisement_data: handle_device(device, advertisement_data, company_identifiers))

    await scanner.start()

    try:
        while True:
            print_active_devices()  # Periodically refresh the active devices list
            await asyncio.sleep(1)
    finally:
        await scanner.stop()

# Main entry point
try:
    asyncio.run(scan_ble_devices())
except KeyboardInterrupt:
    print("\nExiting...")