from firebase_admin import initialize_app, credentials, db
from datetime import datetime


class Firebase:
    def __init__(self, firebase_url, path_to_service_account, current_month):
        self.firebase_url = firebase_url
        self.path_to_service_account = path_to_service_account
        self.rtdb = self.initialize_connection()
        if self.rtdb.get() == None:
            self.rtdb.child("property_listings").set("")
            self.rtdb.child("api_calls").set(
                {
                    "current_month": current_month,
                    "num_calls": 0,
                    "time_of_last_call": "1000-01-01 00:00",
                }
            )

    def initialize_connection(self):
        # initialize connection through a service account
        cred = credentials.Certificate(self.path_to_service_account)
        initialize_app(cred, {"databaseURL": self.firebase_url})
        return db.reference("/")

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
        """Add the property address and detargument as a new node under the 'property_listings' child."""
        self.rtdb.child("property_listings").push(property_details)

    def update_month_in_db(self, current_month):
        """Update the month for which api calls are being tracked to the current month."""
        self.rtdb.child("api_calls").child("current_month").set(current_month)

    def update_num_api_calls_made(self, api_calls):
        """Add the api_call to the database"""
        self.rtdb.child("api_calls").child("num_calls").set(api_calls)

    def update_time_of_last_call(self, api_call_datetime_string):
        """Update the time that the last api call was made as the current datetime converted to string to the database."""
        self.rtdb.child("api_calls").child("time_of_last_call").set(
            api_call_datetime_string
        )

    def remove_property_from_database(self, UID):
        """Delete a specific node under the 'property_addresses' child, given its UID."""
        self.rtdb.child(f"property_listings/{UID}").delete()
