# darkweb_monitoring.py

import random

# Some simulated dark web results
SIMULATED_DARK_WEB_ENTRIES = [
    {"site": "darkmarket.onion", "description": "Leaked credentials"},
    {"site": "blackforums.onion", "description": "Stolen user data"},
    {"site": "onionmail.org", "description": "Mentions of phishing attack"},
    {"site": "darkvault.onion", "description": "Financial info exposed"},
    {"site": "hackershub.onion", "description": "Database leak detected"},
]

def monitordarkweb(keyword: str):
    """
    Simulate a dark web search for a given keyword.
    """
    if not keyword:
        return {"error": "Keyword is required", "status": "error"}

    # Randomly decide if there are matches (50% chance)
    found = random.choice([True, False])

    if found:
        results = random.sample(SIMULATED_DARK_WEB_ENTRIES, k=random.randint(1, 3))
        return {
            "query": keyword,
            "status": "Potential dark web mentions found",
            "results": results
        }
    else:
        return {
            "query": keyword,
            "status": "No dark web results found",
            "results": []
        }
