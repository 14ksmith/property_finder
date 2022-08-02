from dotenv import load_dotenv
import os
from database import Firebase
from property_results import (
    call_realty_mole_api,
    email_formatted_property_results,
    filter_api_results,
    hours_between_api_requests,
)
from datetime import datetime, timedelta
from time import sleep

seconds_between_api_requests = hours_between_api_requests * 60 * 60

# Infinite while loop that runs the program and then sleeps for the hours designated between api calls
while True:

    current_datetime = datetime.now()
    current_month = current_datetime.strftime("%B")

    # ----------------------------- LOAD ENV VARIABLES -------------------------------------#

    # load environment variables from .env
    load_dotenv()

    # ----------------------------- CONNECT TO THE  DB -------------------------------------#

    # create the firebase connection
    firebase = Firebase(
        os.getenv("FIREBASE_RTDB_URL"),
        os.getenv("PATH_TO_FIREBASE_SERVICE_ACCOUNT"),
        current_month=current_month,
    )

    # ----------------------------- API CALL SCHEDULE --------------------------------------#

    # Get the datetime object of when the last api call was made from the database
    datetime_of_last_api_call = firebase.get_time_of_last_api_call()

    # if the datetime of the last api call made plus the specified hours between calls is <= the current datetime, make api call
    if (
        datetime_of_last_api_call + timedelta(hours=hours_between_api_requests)
        <= current_datetime
    ):

        # ------------------------ GET MONTH AND NUM API CALLS FROM DB -------------------------#

        # if the month in the database does not equal the current month, then update the month in the db
        month_in_db = firebase.get_month_from_db()
        if month_in_db != current_month:
            firebase.update_month_in_db(current_month=current_month)

        # Get the number api calls made this month by calling get_num_api_calls_from_db
        # TODO: if the number is at the max set in configure.json, send a email saying they have reached their max for the month
        num_api_calls_in_db = firebase.get_num_api_calls_from_db()

        # ----------------------------- SEND API REQUESTS --------------------------------------#

        # run the call_realty_mole_api function, returns the results of the search and the number of new api calls made
        call_realty_mole_api = call_realty_mole_api(
            num_api_calls_in_db=num_api_calls_in_db
        )
        # First value in tuple returned from function is the property results, which will be set to 'filtered_property_results'
        all_search_results = call_realty_mole_api[0]
        # Second value in tuple returned from function is the number of new calls made to the api
        num_api_calls_made = call_realty_mole_api[1]
        # Third value in tuple returned from funtion is the datetime object when the api calls were made
        api_call_datetime_string = call_realty_mole_api[2]

        # ----------------------------- FILTER API REQUESTS --------------------------------------#

        # if api call was made and there are results in all_search_results...
        if all_search_results:

            # update the time that the api calls were made to the current datetime
            firebase.update_time_of_last_call(
                api_call_datetime_string=api_call_datetime_string
            )

            # Run the method to filter through the api results given the params set in configure.json, and set results to filtered_property_results
            filtered_property_results = filter_api_results(
                all_search_results=all_search_results
            )

            # ----------------------------- EMAIL FILTERED RESULTS -------------------------------------#

            # Email the filtered property results, and set the addresses returned from this function to 'property_addresses'
            property_results = email_formatted_property_results(
                filtered_property_results=filtered_property_results
            )

            # ----------------------------- GET ADDRESSES ALREADY IN  DB --------------------------------#

            # Retrieve the properties that are already in the database
            properties_in_db = firebase.get_properties_from_db()

            # ----------------------------- ADD NEW ADDRESSES TO  DB -------------------------------------#

            # for every address and details returned from the email_formatted_property_results method:
            for address_details in property_results:
                # If the address and details is not already in the list of property addresses in the database:
                if address_details not in properties_in_db:
                    # Add the address and details to the database
                    firebase.add_property_to_db(property_details=address_details)

            # ----------------------------- UPDATE API REQUEST NUM IN DB ---------------------------------#

            # Update the number of api calls made in the month to the database
            firebase.update_num_api_calls_made(api_calls=num_api_calls_made)

    # Sleep the program for the designated time between api calls
    sleep(seconds_between_api_requests)
