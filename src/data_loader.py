import requests
import pandas as pd

# Catapult API Key
CATAPULT_API_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0NjFiMTExMS02ZjdhLTRkYmItOWQyOS0yMzAzOWZlMjI4OGUiLCJqdGkiOiI2N2Q0NDI0MTVhZmU4MDZkY2IwYWI4OTk2NDQ2NWNlZmVhYzk0MDk0MmMyOGM2ZDU0MjY2NjI5NDU1MDdjYTcwNDU4MzYxZWQ0NjMwNWQxYSIsImlhdCI6MTczODA5ODYwMS42NTc1NjMsIm5iZiI6MTczODA5ODYwMS42NTc1NjUsImV4cCI6NDg5MTY5ODYwMS42NDc3MTgsInN1YiI6ImFkOGFhNGNhLTMzNTEtNDYyMC1iNWM2LTFiMzE0Zjk0ZDNlZCIsInNjb3BlcyI6WyJjb25uZWN0Iiwic2Vuc29yLXJlYWQtb25seSIsImF0aGxldGVzLXVwZGF0ZSIsInRhZ3MtdXBkYXRlIiwiYWN0aXZpdGllcy11cGRhdGUiLCJhbm5vdGF0aW9ucy11cGRhdGUiLCJwYXJhbWV0ZXJzLXVwZGF0ZSJdfQ.xVsyPtoG_dleeI4o80flQ0sN7zsfQJlsssCKZTeJpoZgE2yyRruF70MvYlUIcDtTNfZgAH9Jgao6lGP168oZw9Qpu4_izbCceyH6IEKamRzC_yRj_f_sAga3pO2sDeHvCuP2YCe9jcWiNiCsC8mDsjDPAvwOfMiur8V3PqssvoLrNMtc-9aYMzfGBs1ZY_O4XsgX1EGw4dGe_4fC5DvtA3xs_pD3KIi76APnUXieq0jRO1lSENu_1Uge8AsQZfthSlr6CiaAHQzTS8UIawNbO-7bPFICHmdGRXTDYnOF2WkgqtXbHIPjkaCk3rJeWtoj2QYPbp9uvpglXDT5KEoCu5_EW8DrXBSTwC8FuYPU-ow741zR-Xjl_3AT4H-3kqeQOXGas7EbkUTRjyPFdFuPVctjnYjth3vV4sqtfCLt54in2XJQGbtwQ7j-feHZq1ZB8ps205MmwSJA90dRbdLKmGmLd9iRG_nvSs1nQ3EvUqLRB5KBjd0lHyTAjdA6WJlHvHakTspApw_3PEeNTHeDuYf-AirHyzyyVZzu6-FG4li_nFTzAd2dmd-dPaQAPvZr6_Jy74agBjzxHlKVd59uGOsTbTzjdluDzhw2t_N4ETY2wc_76yZziQVbxG1ELykN53rZ5kX-7hPltsE5CXAt76cB9KyoHYPAo5PLCy7ZxwU"  # Replace with your full API key

# Base URL for the Catapult API
CATAPULT_BASE_URL = "https://connect-us.catapultsports.com/api/v6"

# Fetch data from a specific endpoint
def fetch_catapult_data(endpoint_path):
    """
    Fetch data from a given endpoint in the Catapult API.
    """
    headers = {"Authorization": f"Bearer {CATAPULT_API_KEY}"}
    url = f"{CATAPULT_BASE_URL}{endpoint_path}"

    print(f"Requesting URL: {url}")
    print(f"Headers: {headers}")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error details: {response.text}")
        raise Exception(f"Error fetching data from Catapult API: {response.status_code}, {response.text}")

# Example function to fetch athlete data
def fetch_athletes():
    """
    Fetch the list of athletes from the Catapult API.
    :return: DataFrame of athletes.
    """
    athletes = fetch_catapult_data("/athletes")
    return pd.DataFrame(athletes)

# Example function to fetch activities
def fetch_activities():
    """
    Fetch the list of activities from the Catapult API.
    :return: DataFrame of activities.
    """
    activities = fetch_catapult_data("/activities")
    return pd.DataFrame(activities)