from unittest.mock import call
import requests
from initialize import initialize_settings, set_api_requirements
from send_email import send_email
from datetime import datetime

config_settings = initialize_settings()


def call_realty_mole_api(num_api_calls_in_db):
    """Make an api call for each location parameter in configure.json, as long as making the call will not overshoot the max montly calls.
    Return a list of json results and the number of new api calls made."""

    # Set variable for the max monthly api calls from configure.json
    max_api_calls_per_month = config_settings.get("monthly_request_limit")
    print(type(max_api_calls_per_month))

    # Get the api request requirements from initialize.py
    api_requirements_dict = set_api_requirements()

    # Get and keep track of the number of api calls that are recorded in the database
    num_api_calls_made = num_api_calls_in_db
    print(type(num_api_calls_made))

    # For each unique search paramater (location) in search_params, get the info from the api
    for params in config_settings.get("search_params"):

        # if the number of api calls recorded in the database plus 1 is <= max api calls per month, send the api request
        if (num_api_calls_made + 1) <= max_api_calls_per_month:
            # Get Realty Mole API data
            response = requests.get(
                url=api_requirements_dict.get("realty_mole_API"),
                params=params,
                headers=api_requirements_dict.get("headers"),
            )
            # Check status of request
            response.raise_for_status
            # create data variable to hold json data from response
            property_search_results = response.json()

            # Keep track of the number of api calls being made (1 for each search param) and add it to api_calls_in_db
            num_api_calls_made += 1

        # If the number will exceede the max api calls per month, then break out of the for-loop
        else:
            break

    return property_search_results, num_api_calls_in_db


def filter_api_results(property_search_results):
    """Using the search params from configure.json, filter through the api results and return only those that fit within the params."""

    # List of property results after filtering through the user's search parameters (price, beds, baths, etc)
    filtered_property_results = []

    for result in property_search_results:
        if (
            result.get("price") != None
            and result.get("price") <= config_settings.get("max_price")
            and result.get("propertyType") != None
            and result.get("propertyType") == config_settings.get("home_type")
            and result.get("bedrooms") != None
            and result.get("bedrooms") >= config_settings.get("num_beds")
            and result.get("bathrooms") != None
            and result.get("bathrooms") >= config_settings.get("num_baths")
        ):
            # if the result matches all of the above requirements, add it to the 'filtered_property_results' list
            filtered_property_results.append(result)

    return filtered_property_results


def email_formatted_property_results(filtered_property_results):
    """Send the email with the formatted property results. Return the list of formatted property addresses."""

    # Create empty string for where the formatted property results with go for the email body
    string_of_formatted_property_results = ""
    # Create list of just property addresses
    property_results_list = []

    # For each property from the filtered_property_settings...
    for property in filtered_property_results:
        # Get all of the necessary
        property_address = property.get("formattedAddress")
        property_price = property.get("price")
        property_bedrooms = property.get("bedrooms")
        property_bathrooms = property.get("bathrooms")
        property_sq_footage = property.get("squareFootage")
        # Have to format property id to remove city, or else the zillow link does not work
        property_id = "".join(property.get("id").split(",")[0::2])
        # create the zillow link for each property from the list
        property_zillow_link = f"https://www.zillow.com/homes/{property_id}"
        # how each property result should be formatted for the email
        string_of_formatted_property_results += f"{property_address}\nPrice: ${property_price}\nBedrooms: {property_bedrooms}\nBathrooms: {property_bathrooms}\nSquare Footage: {property_sq_footage}\nZillow Link: {property_zillow_link}\n\n"
        # Add the formated property address to the list
        property_results_list.append(
            {
                "address": property_address,
                "zillow_link": property_zillow_link,
                "price": f"${property_price}",
                "bedrooms": property_bedrooms,
                "bathrooms": property_bathrooms,
                "sq_footage": property_sq_footage,
            }
        )

    send_email(
        email_body=string_of_formatted_property_results,
        server=config_settings.get("server"),
    )
    return property_results_list


def api_call_schedule(current_date, api_calls_in_db):
    """Follow the schedule of api request frequency each week, without going over the max number of monthly calls."""
    api_calls_per_week = config_settings.get("request_frequency_per_week")
    max_api_calls_per_month = config_settings.get("montly_request_limit")
    num_search_params = len(config_settings.get("search_params"))

    if (api_calls_in_db + num_search_params) <= max_api_calls_per_month:
        # run the call_realty_mole_api function
        call_realty_mole_api = call_realty_mole_api()
        # First value in tuple returned from function is the property results, which will be set to 'filtered_property_results'
        filtered_property_results = call_realty_mole_api[0]
