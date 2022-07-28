import requests
from initialize import get_settings_params, set_api_requirements
from send_email import send_email


def get_filtered_property_results():
    """For each location, filter through property results from API with specifications applied from configure.json. Return the list of filtered results."""
    # Get settings dict from get_settings_params and set as settings_dict
    settings_dict = get_settings_params()

    api_requirements_dict = set_api_requirements()

    # List of property results after filtering through the user's search parameters (price, beds, baths, etc)
    filtered_property_results = []

    # For each unique search paramater (location) in search_params, get the info from the api
    for params in settings_dict.get("search_params"):
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
        # print all data from json result
        for result in property_search_results:
            # TODO: add if result["lastSeen"] == current date
            if (
                result.get("price") != None
                and result.get("price") <= settings_dict.get("max_price")
                and result.get("propertyType") != None
                and result.get("propertyType") == settings_dict.get("home_type")
                and result.get("bedrooms") != None
                and result.get("bedrooms") >= settings_dict.get("num_beds")
                and result.get("bathrooms") != None
                and result.get("bathrooms") >= settings_dict.get("num_baths")
            ):
                # if the result matches all of the above requirements, add it to the 'filtered_property_results' list
                filtered_property_results.append(result)

    return filtered_property_results


def email_formatted_property_results(filtered_property_results):
    """Send the email with the formatted property results. Return the list of formatted property addresses."""
    # Get settings dict from get_settings_params and set as settings_dict
    settings_dict = get_settings_params()

    # Create empty string for where the formatted property results with go for the email body
    string_of_formatted_property_results = ""
    # Create list of just property addresses
    property_addresses_list = []

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
        property_addresses_list.append(property_address)

    send_email(
        email_body=string_of_formatted_property_results,
        server=settings_dict.get("server"),
    )
    return property_addresses_list
