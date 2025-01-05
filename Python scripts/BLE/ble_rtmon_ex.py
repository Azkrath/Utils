from bleak import BleakScanner
import time, os, asyncio, yaml

# Track active devices
active_devices = {}

# Timeout for removing inactive devices (seconds)
DEVICE_TIMEOUT = 10

# Function to load the manufacturer data from a YAML file
def load_company_identifiers(file_name):
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory where the script is located
    file_path = os.path.join(script_dir, file_name)  # Combine with the YAML file name
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
# Function to handle device detection
def handle_device(device, advertisement_data, company_identifiers):
    current_time = time.time()
    manufacturer = "Unknown"

    # Extract manufacturer ID from advertisement data (example: 16-bit manufacturer ID)
    manufacturer_id = None
    
    if advertisement_data.manufacturer_data:
        for manuf_id in advertisement_data.manufacturer_data.items():
            # The key `manuf_id` is the 16-bit manufacturer ID
            manufacturer_id = manuf_id
            break  # Assuming only one manufacturer ID in the advertisement

    if manufacturer_id is not None:
        # Lookup the manufacturer based on the assigned number
        manufacturer = get_manufacturer_from_id(manufacturer_id, company_identifiers)

    # Use rssi from advertisement_data instead of device.rssi
    active_devices[device.address] = {
        "name": device.name or "Unknown",
        "manufacturer": manufacturer,
        "rssi": advertisement_data.rssi,  # Updated here
        "last_seen": current_time,
    }

# Function to get manufacturer from the ID using the loaded YAML data
def get_manufacturer_from_id(manufacturer_id, company_identifiers):
    for entry in company_identifiers:
        if entry['value'] == manufacturer_id:
            return entry['name']
    return "Unknown Manufacturer"

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
            f"Device: {address} | Name: {info['name']} | Manufacturer: {info['manufacturer']} | RSSI: {info['rssi']} dBm"
        )

    # Remove timed-out devices
    for address in to_remove:
        del active_devices[address]

    print("=" * 40)
    print("Press Ctrl+C to stop.")

# Asynchronous BLE scanning function
async def scan_ble_devices():
    print("Reading company identifiers...")
    company_identifiers = load_company_identifiers('vendors.yaml')

    print("Initializing BLE Scanner...")
    scanner = BleakScanner()

    # Pass the loaded company_identifiers to the callback
    scanner.register_detection_callback(lambda device, advertisement_data: handle_device(device, advertisement_data, company_identifiers))
    

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