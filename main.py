from xml.sax.handler import property_declaration_handler
from dotenv import load_dotenv
import os
from database import Firebase
from property_results import (
    call_realty_mole_api,
    email_formatted_property_results,
    filter_api_results,
)
import json
from datetime import datetime

current_month = datetime.now().strftime("%B")
print(current_month)


# load environment variables from .env
load_dotenv()

# create the firebase connection
firebase = Firebase(
    os.getenv("FIREBASE_RTDB_URL"),
    os.getenv("PATH_TO_FIREBASE_SERVICE_ACCOUNT"),
    current_month=current_month,
)

# Get the number api calls made this month by calling get_num_api_calls_from_db
num_api_calls_in_db = firebase.get_num_api_calls_from_db()


# run the call_realty_mole_api function, returns the results of the search and the number of new api calls made
call_realty_mole_api = call_realty_mole_api(num_api_calls_in_db=num_api_calls_in_db)
# First value in tuple returned from function is the property results, which will be set to 'filtered_property_results'
property_search_results = call_realty_mole_api[0]
# Second value in tuple returned from function is the number of new calls made to the api
num_api_calls_made = call_realty_mole_api[1]


# Run the method to filter through the api results given the params set in configure.json, and set results to filtered_property_results
filtered_property_results = filter_api_results(
    property_search_results=property_search_results
)


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

# Update the number of api calls made in the month to the database
firebase.update_num_api_calls_made(api_calls=num_api_calls_made)
