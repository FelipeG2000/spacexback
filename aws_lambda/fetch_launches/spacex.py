import requests

rocket_cache = {}
launchpad_cache = {}

def fetch_launches():
    url = "https://api.spacexdata.com/v4/launches"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_rocket_name(rocket_id):
    if not rocket_id:
        return "Unknown"
    if rocket_id in rocket_cache:
        return rocket_cache[rocket_id]
    try:
        rocket_url = f"https://api.spacexdata.com/v4/rockets/{rocket_id}"
        response = requests.get(rocket_url)
        response.raise_for_status()
        name = response.json().get("name", "Unknown")
        rocket_cache[rocket_id] = name
        return name
    except Exception as e:
        print(f"Error fetching rocket {rocket_id}: {e}")
        return f"ID: {rocket_id}"

def get_launchpad_name(launchpad_id):
    if not launchpad_id:
        return "Unknown"
    if launchpad_id in launchpad_cache:
        return launchpad_cache[launchpad_id]
    url = f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}"
    response = requests.get(url)
    response.raise_for_status()
    name = response.json().get("name", "Unknown")
    launchpad_cache[launchpad_id] = name
    return name
