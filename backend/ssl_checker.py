import requests
import time

def check_ssl(domain):
    url = f"https://api.ssllabs.com/api/v3/analyze?host={domain}&all=done"
    
    # Initial request to start the scan
    response = requests.get(url)
    data = response.json()
    
    # Wait for the scan to complete
    while data.get("status") == "IN_PROGRESS":
        print("🔍 Scanning... Please wait.")
        time.sleep(10)  # Wait 10 seconds before checking again
        response = requests.get(url)
        data = response.json()

    return data  # Return final scan results

# Example usage:
result = check_ssl("tryhackme.com")
print(result)
