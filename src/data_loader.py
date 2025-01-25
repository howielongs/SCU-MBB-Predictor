import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API credentials
CLIENT_ID = os.getenv("VALD_CLIENT_ID")
CLIENT_SECRET = os.getenv("VALD_CLIENT_SECRET")
AUTH_URL = "https://prd-use-api-extsmartspeed.valdperformance.com/authentication"

# Authentication function
def authenticate():
    response = requests.post(
        AUTH_URL,
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials",
        },
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception(f"Authentication failed: {response.status_code}")

# Fetch data from a specific endpoint
def fetch_api_data(token, base_url, endpoint_path):
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{base_url}{endpoint_path}"  # Combine base URL with endpoint path
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}")
