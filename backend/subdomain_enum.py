import requests

def get_subdomains(domain):
    urls = [
        f"https://api.hackertarget.com/hostsearch/?q={domain}",
        f"https://crt.sh/?q={domain}&output=json"  # crt.sh alternative
    ]

    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            if "hackertarget" in url:
                subdomains = [line.split(",")[0] for line in response.text.split("\n") if line]
            else:  # crt.sh API returns JSON
                subdomains = [entry["name_value"] for entry in response.json()]

            return list(set(subdomains))  # Remove duplicates
        except requests.exceptions.RequestException:
            continue  # Try the next API if one fails

    return {"error": "All subdomain enumeration APIs failed"}
