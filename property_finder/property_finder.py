from datetime import datetime, timedelta
from calendar import monthrange
from database.database import firebase
from time import sleep
import json
from notifications.email import send_email
from datetime import datetime
from property_finder.property_api import call_realty_mole_api
import asyncio


class Property_Search_Settings:
    def __init__(self):

        # Get the settings from the property search settings json
        with open("property_search_settings.json") as config:
            property_search_settings = json.load(config)

        # Get the wait time between searches in hours
        self.hours_between_api_requests = property_search_settings.get(
            "hours_between_api_requests"
        )

        # Multiply hours by 60 * 60 to get sleep time in seconds
        self.seconds_between_api_requests = self.hours_between_api_requests * 60 * 60

        # set the monthly request limit for api calls variable
        self.monthly_request_limit = property_search_settings.get(
            "monthly_request_limit"
        )

        # set the realty mole account creation day variable
        self.api_account_roll_over_day = property_search_settings.get(
            "realty_mole_account_creation_day"
        )

        # initialize the search params
        self.search_params = property_search_settings.get("search_params")
        self.price_limit = property_search_settings.get("price_limit")
        self.home_type = property_search_settings.get("home_type")
        self.min_num_beds = property_search_settings.get("min_num_beds")
        self.min_num_baths = property_search_settings.get("min_num_baths")

        # initialize the email server to send email notifications
        self.email_server = property_search_settings.get("email_server")


def filter_api_results(
    all_search_results,
    addresses_in_db,
    property_search_settings: Property_Search_Settings,
):
    """Using the search params from property_search_settings.json, filter through the api results and return only those that fit within the params and are not already in the database."""

    # List of property results after filtering through the user's search parameters (price, beds, baths, etc)
    filtered_property_results = []

    # For each location in all_search_results
    for search_location in all_search_results:
        print(search_location)
        # For each result returned for search_location
        for result in search_location:
            print(result)
            if (
                # The address is not already in the database...
                result.get("formattedAddress") not in addresses_in_db
                # and the results match the requirements outlined in property_search_settings.json...
                and result.get("price") != None
                and result.get("price") <= property_search_settings.price_limit
                and result.get("propertyType") != None
                and result.get("propertyType") == property_search_settings.home_type
                and result.get("bedrooms") != None
                and result.get("bedrooms") >= property_search_settings.min_num_beds
                and result.get("bathrooms") != None
                and result.get("bathrooms") >= property_search_settings.min_num_baths
            ):
                # if the result matches all of the above requirements, add it to the 'filtered_property_results' list
                filtered_property_results.append(result)

    return filtered_property_results


def email_formatted_property_results(filtered_property_results, email_server):
    """Send the email with the formatted property results. Return the list of formatted property results."""

    # Create empty string for where the formatted property results with go for the email body
    email_body = ""

    # Create list of formatted property results
    property_results_list = []

    # If the filtered_property_results list is not empty...
    if filtered_property_results:

        # For each property from the filtered_property_results...
        for property in filtered_property_results:
            # Get all of the necessary info
            property_address = property.get("formattedAddress")
            property_price = property.get("price")
            property_bedrooms = property.get("bedrooms")
            property_bathrooms = property.get("bathrooms")
            property_sq_footage = property.get("squareFootage")
            # Have to format property id to remove city, or else the zillow link does not work
            property_id = "".join(property.get("id").split(",")[0::2])
            # create the zillow link for each property from the list
            property_zillow_link = f"https://www.zillow.com/homes/{property_id}"
            # how each property result should be formatted for the email, and add it to 'email_body'
            email_body += f"{property_address}\nPrice: ${property_price}\nBedrooms: {property_bedrooms}\nBathrooms: {property_bathrooms}\nSquare Footage: {property_sq_footage}\nZillow Link: {property_zillow_link}\n\n"
            # Add the formated property results to the list
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

    else:
        email_body = (
            "There are no new property results that fit your request at this time."
        )

    # Send an email with the results
    send_email(email_body=email_body, server=email_server)

    return property_results_list


def reset_api_usage_back_to_0(
    current_month_number,
    current_year,
    current_day,
    property_search_settings,
):
    """If the current day of the month is equal to the realty_mole_account_creation_day in property_search_settings.json, reset the num_calls to 0 in db.
    If that date is not in the current month, then reset the num_calls to 0 on the last day of the month."""

    # if the number of days in the month DOES include the realty mole api account creation day
    if property_search_settings in range(
        0, monthrange(year=current_year, month=(current_month_number))[1] + 1
    ):
        # Update num_calls to 0 on the creation date each
        if property_search_settings == current_day:
            firebase.update_num_api_calls_made(0)

    # if the number of days in the month does NOT include the api account creation day
    else:
        # Update the num_calls to 0 on the last day of the month
        if (
            current_day
            == monthrange(year=current_year, month=(current_month_number))[1]
        ):
            firebase.update_num_api_calls_made(0)


async def find_properties():
    property_search_settings = Property_Search_Settings()

    # Infinite while loop that sleeps for user designated period of time (hours converted to seconds)
    while True:
        # Get the current month to track how many api calls have been made to the property api this month.
        current_datetime = datetime.now()
        current_month = current_datetime.strftime("%B")
        current_month_number = int(current_datetime.strftime("%m"))
        current_day = int(current_datetime.strftime("%d"))
        current_year = int(current_datetime.strftime("%Y"))

        # Get the datetime object of when the last api call was made from the database from the local variable
        datetime_of_last_api_call = firebase.time_of_last_api_call_in_db

        # if the datetime of the last api call made plus the specified hours between calls is <= the current datetime, make api call
        if (
            datetime_of_last_api_call
            + timedelta(hours=property_search_settings.hours_between_api_requests)
            <= current_datetime
        ):

            # if the month in the database local variable does not equal the current month, then update the month in the db
            if firebase.api_month != current_month:
                firebase.update_month_in_db(current_month=current_month)

            # If it is the correct date, set the num_calls in the database back to 0
            reset_api_usage_back_to_0(
                current_day=current_day,
                current_month_number=current_month_number,
                current_year=current_year,
                property_search_settings=property_search_settings.api_account_roll_over_day,
            )

            # run the call_realty_mole_api function, returns the results of the search and the number of new api calls made
            realty_mole_api_result = call_realty_mole_api(
                num_api_calls_in_db=firebase.number_of_api_calls_in_current_month,
                monthly_request_limit=property_search_settings.monthly_request_limit,
                search_params=property_search_settings.search_params,
                email_server=property_search_settings.email_server,
            )

            # First value in tuple returned from function is the property results, which will be set to 'filtered_property_results'
            all_search_results = realty_mole_api_result[0]

            # Update the total number of api calls made this month to the database
            #       Second value in tuple returned from function is the number of total calls made to the api for the month
            firebase.update_num_api_calls_made(realty_mole_api_result[1])

            # Third value in tuple returned from funtion is the datetime object when the api calls were made
            api_call_datetime_string = realty_mole_api_result[2]

            # if api call was made and there are results in all_search_results...
            if all_search_results:

                # Retrieve the properties that are already in the database from the local variable
                addresses_in_db = firebase.stored_addresses

                # update the time that the api calls were made to the datetime returned from call_realty_mole_api
                firebase.update_time_of_last_call(
                    api_call_datetime_string=api_call_datetime_string
                )

                # Run the method to filter through the api results given the params set in configure.json, and set results to filtered_property_results
                filtered_property_results = filter_api_results(
                    all_search_results=all_search_results,
                    addresses_in_db=addresses_in_db,
                    property_search_settings=property_search_settings,
                )

                # Email the filtered property results, and set the addresses returned from this function to 'property_addresses'
                property_results = email_formatted_property_results(
                    filtered_property_results=filtered_property_results,
                    email_server=property_search_settings.email_server,
                )

                # if there are results in the property_results list, do the following
                if property_results:

                    # add a list of coroutines to complete
                    tasks = []

                    # for every address and details returned from the email_formatted_property_results method:
                    for address_details in property_results:
                        # append the add_property_to_db async function to the list of tasks
                        # Add the address and details to the database
                        tasks.append(
                            firebase.add_property_to_db(
                                property_details=address_details
                            )
                        )

                    # execute all the tasks and wait for them to complete
                    asyncio.wait(tasks)

        # Sleep the program for the designated time between api calls
        sleep(property_search_settings.seconds_between_api_requests)
