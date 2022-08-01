from firebase_admin import initialize_app, credentials, db


class Firebase:
    def __init__(self, firebase_url, path_to_service_account):
        self.firebase_url = firebase_url
        self.path_to_service_account = path_to_service_account
        self.rtdb = self.initialize_connection()
        if self.rtdb.get() == None:
            self.rtdb.child("property_listings").set("")
            self.rtdb.child("api_calls").set("")

    def initialize_connection(self):
        # initialize connection through a service account
        cred = credentials.Certificate(self.path_to_service_account)
        initialize_app(cred, {"databaseURL": self.firebase_url})
        return db.reference("/")

    def get_properties_from_db(self):
        """Get all nodes from the 'property_addresses' child, then add the value (address) from each to the 'list_of_addresses' and retun list."""
        properties_in_db = self.rtdb.child("property_listings").get()

        if properties_in_db == None:
            pass
        else:
            list_of_addresses = [
                properties_in_db[property_id] for property_id in properties_in_db
            ]
        return list_of_addresses

    def add_property_to_db(self, property_details):
        """Add the property address and detargument as a new node under the 'property_listings' child."""
        self.rtdb.child("property_listings").push(property_details)

    def add_api_call_to_db(self, api_call):
        """Add the api_call to the database"""
        self.rtdb.child("api_calls").push(api_call)

    def remove_property_from_database(self, UID):
        """Delete a specific node under the 'property_addresses' child, given its UID."""
        self.rtdb.child(f"property_listings/{UID}").delete()
