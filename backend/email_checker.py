import requests

# Use your API key from Abstract API
API_KEY = "2eaa650b9e67451093953a5afd95a62d"
BASE_URL = "https://emailvalidation.abstractapi.com/v1/"


def check_email(email):
    url = f"{BASE_URL}?api_key={API_KEY}&email={email}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Convert quality score to percentage
        quality_score_percentage = float(data.get("quality_score", 0)) * 100
        
        # Add percentage format to response
        data["quality_score_percentage"] = f"{quality_score_percentage:.2f}%"
        
        return data
    else:
        return {"error": "Failed to fetch email validation data"}
