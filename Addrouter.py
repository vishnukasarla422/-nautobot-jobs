import requests
import json

# ─── CONFIG ───────────────────────────────────────────────
NAUTOBOT_URL = "http://localhost:8081"
TOKEN = "d8705599a3ec2b8e17d20af56454e1676827dd17"

HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
}

# ══════════════════════════════════════════════════════════ß
#  DEVICES
# ══════════════════════════════════════════════════════════

def get_all_devices():
    """Get all devices in Nautobot"""
    r = requests.get(f"{NAUTOBOT_URL}/api/dcim/devices/", headers=HEADERS)
    data = r.json()
    print(f"\n📋 Total Devices: {data['count']}")
    for d in data['results']:
        print(f"   - {d['name']} | ID: {d['id']}")
    return data['results']


def get_device_by_name(name):
    """Get a specific device by name"""
    r = requests.get(f"{NAUTOBOT_URL}/api/dcim/devices/?name={name}", headers=HEADERS)
    results = r.json()['results']
    if results:
        print(f"✅ Found device: {results[0]['name']} | ID: {results[0]['id']}")
        return results[0]
    print(f"❌ Device '{name}' not found")
    return None


def add_device(name, device_type_id, role_id, location_id, status="Active"):
    """Add a new device"""
    payload = {
        "name": name,
        "device_type": {"id": device_type_id},
        "role": {"id": role_id},
        "location": {"id": location_id},
        "status": {"name": status},
    }
    r = requests.post(f"{NAUTOBOT_URL}/api/dcim/devices/", headers=HEADERS, json=payload)
    if r.status_code == 201:
        d = r.json()
        print(f"✅ Device '{name}' created | ID: {d['id']}")
        return d
    print(f"❌ Failed: {r.status_code} - {r.text}")
    return None


def update_device(device_id, data):
    """Update a device (partial update)"""
    r = requests.patch(f"{NAUTOBOT_URL}/api/dcim/devices/{device_id}/", headers=HEADERS, json=data)
    if r.status_code == 200:
        print(f"✅ Device updated successfully")
        return r.json()
    print(f"❌ Failed: {r.status_code} - {r.text}")
    return None


def delete_device(device_id):
    """Delete a device"""
    r = requests.delete(f"{NAUTOBOT_URL}/api/dcim/devices/{device_id}/", headers=HEADERS)
    if r.status_code == 204:
        print(f"✅ Device deleted successfully")
        return True
    print(f"❌ Failed: {r.status_code} - {r.text}")
    return False


# ══════════════════════════════════════════════════════════
#  IP ADDRESSES
# ══════════════════════════════════════════════════════════

def get_all_ips():
    """Get all IP addresses"""
    r = requests.get(f"{NAUTOBOT_URL}/api/ipam/ip-addresses/", headers=HEADERS)
    data = r.json()
    print(f"\n🌐 Total IPs: {data['count']}")
    for ip in data['results']:
        print(f"   - {ip['address']} | ID: {ip['id']}")
    return data['results']


def add_ip(address, status="Active", description=""):
    """Add a new IP address (e.g. '192.168.1.1/24')"""
    payload = {
        "address": address,
        "status": {"name": status},
        "description": description,
    }
    r = requests.post(f"{NAUTOBOT_URL}/api/ipam/ip-addresses/", headers=HEADERS, json=payload)
    if r.status_code == 201:
        ip = r.json()
        print(f"✅ IP '{address}' created | ID: {ip['id']}")
        return ip
    print(f"❌ Failed: {r.status_code} - {r.text}")
    return None


def assign_primary_ip(device_id, ip_id):
    """Assign an IP as the primary IPv4 of a device"""
    r = requests.patch(
        f"{NAUTOBOT_URL}/api/dcim/devices/{device_id}/",
        headers=HEADERS,
        json={"primary_ip4": {"id": ip_id}}
    )
    if r.status_code == 200:
        print(f"✅ IP assigned as primary IP")
        return r.json()
    print(f"❌ Failed: {r.status_code} - {r.text}")
    return None


# ══════════════════════════════════════════════════════════
#  LOCATIONS
# ══════════════════════════════════════════════════════════

def get_all_locations():
    """Get all locations"""
    r = requests.get(f"{NAUTOBOT_URL}/api/dcim/locations/", headers=HEADERS)
    data = r.json()
    print(f"\n📍 Total Locations: {data['count']}")
    for loc in data['results']:
        print(f"   - {loc['name']} | ID: {loc['id']}")
    return data['results']


# ══════════════════════════════════════════════════════════
#  MANUFACTURERS & DEVICE TYPES
# ══════════════════════════════════════════════════════════

def get_all_manufacturers():
    """Get all manufacturers"""
    r = requests.get(f"{NAUTOBOT_URL}/api/dcim/manufacturers/", headers=HEADERS)
    data = r.json()
    print(f"\n🏭 Total Manufacturers: {data['count']}")
    for m in data['results']:
        print(f"   - {m['name']} | ID: {m['id']}")
    return data['results']


def get_all_device_types():
    """Get all device types"""
    r = requests.get(f"{NAUTOBOT_URL}/api/dcim/device-types/", headers=HEADERS)
    data = r.json()
    print(f"\n🖥️  Total Device Types: {data['count']}")
    for dt in data['results']:
        print(f"   - {dt['model']} | ID: {dt['id']}")
    return data['results']


# ══════════════════════════════════════════════════════════
#  INTERFACES
# ══════════════════════════════════════════════════════════

def get_device_interfaces(device_id):
    """Get all interfaces for a device"""
    r = requests.get(f"{NAUTOBOT_URL}/api/dcim/interfaces/?device_id={device_id}", headers=HEADERS)
    data = r.json()
    print(f"\n🔌 Interfaces for device:")
    for iface in data['results']:
        print(f"   - {iface['name']} | ID: {iface['id']}")
    return data['results']


def add_interface(device_id, name, interface_type="1000base-t"):
    """Add an interface to a device"""
    payload = {
        "device": {"id": device_id},
        "name": name,
        "type": interface_type,
        "status": {"name": "Active"},
    }
    r = requests.post(f"{NAUTOBOT_URL}/api/dcim/interfaces/", headers=HEADERS, json=payload)
    if r.status_code == 201:
        iface = r.json()
        print(f"✅ Interface '{name}' created | ID: {iface['id']}")
        return iface
    print(f"❌ Failed: {r.status_code} - {r.text}")
    return None


# ══════════════════════════════════════════════════════════
#  GENERIC API CALL (for anything not covered above)
# ══════════════════════════════════════════════════════════

def api_get(endpoint):
    """Generic GET - e.g. api_get('/api/dcim/racks/')"""
    r = requests.get(f"{NAUTOBOT_URL}{endpoint}", headers=HEADERS)
    return r.json()


def api_post(endpoint, payload):
    """Generic POST"""
    r = requests.post(f"{NAUTOBOT_URL}{endpoint}", headers=HEADERS, json=payload)
    return r.json()


# ══════════════════════════════════════════════════════════
#  EXAMPLE USAGE
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":

    # --- List everything ---
    get_all_devices()
    get_all_locations()
    get_all_manufacturers()
    get_all_device_types()
    get_all_ips()

    # --- Add a new router ---
    # new_device = add_device(
    #     name="R2",
    #     device_type_id="fa6d7b14-ab29-4e9b-bacb-814a80521ead",  # c7200
    #     role_id="9f301d3a-4c27-4445-94d0-172377e4f3f1",          # Router
    #     location_id="a130951c-9885-4426-a1b8-1101cf6d42e6",      # GNS3-Lab
    # )

    # --- Add IP and assign to device ---
    # ip = add_ip("172.16.115.20/24", description="R2 Management IP")
    # if ip and new_device:
    #     assign_primary_ip(new_device['id'], ip['id'])

    # --- Find device by name ---
    # device = get_device_by_name("R1")

    # --- Delete a device ---
    # delete_device("device-id-here")