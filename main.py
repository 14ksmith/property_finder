from dotenv import load_dotenv
import os
from database import Firebase
from property_results import (
    email_formatted_property_results,
    get_filtered_property_results,
)

# load environment variables from .env
load_dotenv()

# create the firebase connection
firebase = Firebase(
    os.getenv("FIREBASE_RTDB_URL"), os.getenv("PATH_TO_FIREBASE_SERVICE_ACCOUNT")
)

# Return the filtered property results and set to filtered_property_results
filtered_property_results = get_filtered_property_results()

# Email the filtered property results, and set the addresses returned from this function to 'property_addresses'
property_addresses = email_formatted_property_results(
    filtered_property_results=filtered_property_results
)


# Retrieve the properties that are already in the database
properties_in_db = firebase.get_properties_from_db()


# for every address returned from the email_formatted_property_results method:
for address in property_addresses:
    # If the address is not already in the list of property addresses in the database:
    if address not in properties_in_db:
        # Add the address to the database
        firebase.add_property_to_db(address)
