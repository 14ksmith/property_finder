import requests
from dotenv import load_dotenv
import os
from initialize import initialize_settings
from send_email import send_email

# Load environment variables from .env
load_dotenv()

# Set Realty Mole API from .env to 'realty_mole_API'
realty_mole_API = os.getenv("REALTY_MOLE_API")

# Set the header requirements for the api
headers = {
    "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
    "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com",
}
# Get the settings from configure.json and set to 'settings'
settings = initialize_settings()
# Get the search_params from the json file and set to 'search_params'
server = settings["email_server"]
search_params = settings["search_params"]
max_price = settings["price_limit"]
home_type = settings["home_type"]
num_beds = settings["min_num_beds"]
num_baths = settings["min_num_baths"]

# List of property results after filtering through the user's search parameters (price, beds, baths, etc)
filtered_property_results = []

# For each unique search paramater (location) in search_params, get the info from the api
for params in search_params:
    # Get Realty Mole API data
    response = requests.get(url=realty_mole_API, params=params, headers=headers)
    # Check status of request
    response.raise_for_status
    # create data variable to hold json data from response
    property_search_results = response.json()
    # print all data from json result
    for result in property_search_results:
        # TODO: add if result["lastSeen"] == current date
        if (
            result.get("price") != None
            and result.get("price") <= max_price
            and result.get("propertyType") != None
            and result.get("propertyType") == home_type
            and result.get("bedrooms") != None
            and result.get("bedrooms") >= num_beds
            and result.get("bathrooms") != None
            and result.get("bathrooms") >= num_baths
        ):
            # if the result matches all of the above requirements, add it to the 'filtered_property_results' list
            filtered_property_results.append(result)

email_formatted_property_results = []
for property in filtered_property_results:
    property_address = property.get("formattedAddress")
    property_price = property.get("price")
    property_bedrooms = property.get("bedrooms")
    property_bathrooms = property.get("bathrooms")
    property_sq_footage = property.get("squareFootage")
    property_zillow_link = f"https://www.zillow.com/homedetails/{property.get()}"
    email_formatted_property_results += f"{property_address}\nPrice: {property_price}\nBedrooms: {property_bedrooms}\nBathrooms: {property_bathrooms}\nSquare Footage: {property_sq_footage}\nZillow Link: {property_zillow_link}\n\n"

# TODO: check 'lastSeen' date for each address returned in the search and if it is equal to current date, then send it in an email
#           *if it is not equal to the current date, that means it has already been seen by the user so it is not new

send_email(email_body=email_formatted_property_results, server=server)
