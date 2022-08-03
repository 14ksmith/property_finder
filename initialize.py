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


def open_settings():
    """Open configure.json and return the settings as a dictionary."""
    with open("configure.json") as config:
        return json.load(config)
