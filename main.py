import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

realtly_mole_API = os.getenv("REALTY_MOLE_API")

params = {
    "city": "Burlington",
    "state": "VT",
}

headers = {
    "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
    "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com",
}

# Get Realty Mole API data
response = requests.get(url=realtly_mole_API, params=params, headers=headers)
# Check status of request
response.raise_for_status
# create data variable to hold json data from response
data = response.json()
# print all data from json result
print(data)
