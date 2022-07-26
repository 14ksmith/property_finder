import requests
from notifications.email import send_email
from datetime import datetime
import os
from dotenv import load_dotenv


def set_api_requirements():
    """Set API endpoint and Key. Return API and headers in api_requirements_dict"""

    # load environment variables from .env
    load_dotenv()

    api_requirements_dict = dict()

    # Set Realty Mole API from .env to 'realty_mole_API'
    api_requirements_dict["realty_mole_API"] = os.getenv("REALTY_MOLE_API")

    # Set the header requirements for the api
    api_requirements_dict["headers"] = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com",
    }

    return api_requirements_dict


# Initialize the api requirements once when the program starts
api_requirements = set_api_requirements()


def call_realty_mole_api(
    num_api_calls_in_db, monthly_request_limit, search_params, email_server
):
    """Make an api call for each location parameter in configure.json, as long as making the call will not overshoot the max montly calls.
    Return a list of json results for each param and the updated number of total api calls made."""

    # Get current datetime object and turn it into a string
    current_datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Set variable for the max monthly api calls from property_search_settings.json
    max_api_calls_per_month = monthly_request_limit

    # Get the api request requirements
    api_requirements_dict = api_requirements

    # list of all param location search results
    all_search_results = []

    # Get and keep track of the number of api calls that are recorded in the database for the month
    num_api_calls_made_this_month = num_api_calls_in_db

    # For each unique search parameter (location) in search_params, get the info from the api
    for params in search_params:

        # if the number of api calls recorded in the database plus 1 is <= max api calls per month, send the api request
        if num_api_calls_made_this_month + 1 <= max_api_calls_per_month:

            # Get Realty Mole API data
            response = requests.get(
                url=api_requirements_dict.get("realty_mole_API"),
                params=params,
                headers=api_requirements_dict.get("headers"),
            )

            # create data variable to hold json data from response
            property_search_results = response.json()

            # add the results for the param to all_search_results list
            all_search_results.append(property_search_results)

            # Keep track of the number of api calls being made (1 for each search param) and add it to api_calls_in_db
            num_api_calls_made_this_month += 1

        # If the number will exceed the max api calls per month, then send an email saying they have reached their limit
        #       and break out of the for-loop
        else:
            email_body = "You have reached your api request limit for the month."
            send_email(email_body=email_body, server=email_server)
            break

    return all_search_results, num_api_calls_made_this_month, current_datetime_string
