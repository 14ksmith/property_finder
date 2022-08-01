import os
import json


def set_api_requirements():
    """Set API endpoint and Key. Return API and headers in api_requirements_dict"""

    api_requirements_dict = dict()

    # Set Realty Mole API from .env to 'realty_mole_API'
    api_requirements_dict["realty_mole_API"] = os.getenv("REALTY_MOLE_API")

    # Set the header requirements for the api
    api_requirements_dict["headers"] = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "realty-mole-property-api.p.rapidapi.com",
    }

    return api_requirements_dict


def initialize_settings():
    """Open configure.json and return the settings as a dictionary."""
    with open("configure.json") as config:
        return json.load(config)


def get_settings_params():
    """Gets property settings from configure.json and returns them as a dictionary."""
    # Get the settings from configure.json and set to 'settings'
    settings = initialize_settings()
    settings_dict = dict()
    # Get the search_params from the json file and set to 'search_params'
    settings_dict["server"] = settings["email_server"]
    settings_dict["search_params"] = settings["search_params"]
    settings_dict["max_price"] = settings["price_limit"]
    settings_dict["home_type"] = settings["home_type"]
    settings_dict["num_beds"] = settings["min_num_beds"]
    settings_dict["num_baths"] = settings["min_num_baths"]

    return settings_dict
