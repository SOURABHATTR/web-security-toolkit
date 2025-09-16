import requests

# Add your free Shodan API key here
SHODAN_API_KEY = "TQbcVXBmm0p91yX1oT5tOvlikFuKV5aO"

def scan_ports(ip):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extracting open ports
        open_ports = data.get("ports", [])
        return {"ip": ip, "open_ports": open_ports}
    except requests.exceptions.RequestException as e:
        return {"error": f"Port scan failed: {str(e)}"}
