from dotenv import load_dotenv
import os
from firebase_admin import initialize_app, credentials, db
from datetime import datetime


class Firebase:
    def __init__(self):
        # load the environment variables
        load_dotenv()

        # Get the current month to track how many api calls have been made to the property api this month.
        current_datetime = datetime.now()
        current_month = current_datetime.strftime("%B")

        # Set the variables necessary for real time database initalization
        self.firebase_url = os.getenv("FIREBASE_RTDB_URL")
        self.path_to_service_account = os.getenv("PATH_TO_FIREBASE_SERVICE_ACCOUNT")

        # Initialize the firebase connection
        self.rtdb = self.initialize_connection()

        # If the database is empty, initialize realtime database
        #       Set local variables for the database variables
        if self.rtdb.get() == None:
            self.rtdb.child("property_listings").set("")
            self.rtdb.child("api_calls").set(
                {
                    "current_month": current_month,
                    "num_calls": 0,
                    "time_of_last_call": "1000-01-01 00:00",
                }
            )
            self.stored_addresses = None
            self.api_month = current_month
            self.number_of_api_calls_in_current_month = 0
            self.time_of_last_api_call_in_db = "1000-01-01 00:00"
        # If the database is not empty, then get the actual variables from the database for the local variables
        else:
            # Get the addresses that are stored in the database
            self.stored_addresses = self.get_addresses_from_db()
            # Get the month for which the api calls are being tracked in the db.
            self.api_month = self.get_month_from_db()
            # Get the number of api calls recorded in the database
            self.number_of_api_calls_in_current_month = self.get_num_api_calls_from_db()
            # Get the time of the last api call made, which is stored in the database
            self.time_of_last_api_call_in_db = self.get_time_of_last_api_call()

    def initialize_connection(self):
        # initialize connection through a service account
        cred = credentials.Certificate(self.path_to_service_account)
        initialize_app(cred, {"databaseURL": self.firebase_url})
        return db.reference("/")

    # TODO: Cache this locally and then when adding new addresses, update the local value too
    def get_addresses_from_db(self):
        """Get all nodes from the 'property_addresses' child, then add the value (address) from each to the 'list_of_addresses' and retun list."""
        properties_in_db = self.rtdb.child("property_listings").get()

        if properties_in_db == None:
            pass

        else:
            list_of_addresses = [
                properties_in_db[property]["address"] for property in properties_in_db
            ]

        return list_of_addresses

    def get_addresses_from_local_storage(self):
        """Get all addresses that are in the database, stored in the local cache ."""
        return self.stored_addresses

    def get_month_from_db(self):
        """Get the month for which the api calls are being tracked in the db."""
        month_in_db = self.rtdb.child("api_calls").child("current_month").get()
        return month_in_db

    def get_num_api_calls_from_db(self):
        """Get the number of api calls that have been made so far for the month."""
        num_api_calls_in_db = self.rtdb.child("api_calls").child("num_calls").get()
        return num_api_calls_in_db

    def get_time_of_last_api_call(self):
        """Get the time string of the time of last api call from the database, and turn it into datetime object and return it."""
        time_of_last_api_call = (
            self.rtdb.child("api_calls").child("time_of_last_call").get()
        )
        datetime_of_last_api_call = datetime.strptime(
            time_of_last_api_call, "%Y-%m-%d %H:%M"
        )
        return datetime_of_last_api_call

    def add_property_to_db(self, property_details):
        """Add the property address and details as a new node under the 'property_listings' child,
        and add JUST the address to the local variable stored_addresses"""
        self.rtdb.child("property_listings").push(property_details)
        self.stored_addresses.append(property_details["address"])

    def update_month_in_db(self, current_month):
        """Update the month for which api calls are being tracked to the current month,
        and update the local variable api_month."""
        self.rtdb.child("api_calls").child("current_month").set(current_month)
        self.api_month = current_month

    def update_num_api_calls_made(self, num_api_calls):
        """Add the api_call to the database, and update the local variable number_of_api_calls_in_current_month."""
        self.rtdb.child("api_calls").child("num_calls").set(num_api_calls)
        self.number_of_api_calls_in_current_month = num_api_calls

    def update_time_of_last_call(self, api_call_datetime_string):
        """Update the time that the last api call was made as the current datetime converted to string to the database,
        and update the local variable time_of_last_api_call_in_db."""
        self.rtdb.child("api_calls").child("time_of_last_call").set(
            api_call_datetime_string
        )
        self.time_of_last_api_call_in_db = api_call_datetime_string

    def remove_property_from_database(self, UID):
        """Delete a specific node under the 'property_addresses' child, given its UID."""
        self.rtdb.child(f"property_listings/{UID}").delete()


firebase = Firebase()
