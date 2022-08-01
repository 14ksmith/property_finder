from dotenv import load_dotenv
import os
from database import Firebase
from property_results import (
    call_realty_mole_api,
    email_formatted_property_results,
)
import json
from datetime import datetime


# load environment variables from .env
load_dotenv()

# create the firebase connection
firebase = Firebase(
    os.getenv("FIREBASE_RTDB_URL"), os.getenv("PATH_TO_FIREBASE_SERVICE_ACCOUNT")
)

# Open the config file and set the json to settings
with open("configure.json") as config:
    settings = json.load(config)
    # Get the montly_request_limit from the json and set to 'monthly_request_limit'
    monthly_request_limit = settings["monthly_request_limit"]
    # Get the request_frequency_per_week from the json and set to 'weekly_request_frequency'
    weekly_request_frequency = settings["request_frequency_per_week"]

# Get the current month as an int (ex: July is 07)
current_month = datetime.now().strftime("%m")
print(current_month)


# run the call_realty_mole_api function
call_realty_mole_api = call_realty_mole_api()
# First value in tuple returned from function is the property results, which will be set to 'filtered_property_results'
filtered_property_results = call_realty_mole_api[0]
# Second value in tuple returned from function is the datetime object of each api call made when function is called.
num_api_calls = call_realty_mole_api[1]

# Email the filtered property results, and set the addresses returned from this function to 'property_addresses'
property_results = email_formatted_property_results(
    filtered_property_results=filtered_property_results
)


# Retrieve the properties that are already in the database
properties_in_db = firebase.get_properties_from_db()


# for every address and details returned from the email_formatted_property_results method:
for address_details in property_results:
    # If the address and details is not already in the list of property addresses in the database:
    if address_details not in properties_in_db:
        # Add the address and details to the database
        firebase.add_property_to_db(property_details=address_details)

# add the api calls to the database
for api_call in num_api_calls:
    firebase.add_api_call_to_db(api_call=api_call)


# TODO: Add a part of the database that keeps track of how many api calls have been made

# TODO: Add other info from each address to the database
