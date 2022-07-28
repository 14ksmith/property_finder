from firebase_admin import initialize_app, credentials, db


class Firebase:
    def __init__(self, firebase_url, path_to_service_account):
        self.firebase_url = firebase_url
        self.path_to_service_account = path_to_service_account
        self.rtdb = self.initialize_connection()
        if self.rtdb.get() == None:
            self.rtdb.child("property_addresses").set("")

    def initialize_connection(self):
        # initialize connection through a service account
        cred = credentials.Certificate(self.path_to_service_account)
        initialize_app(cred, {"databaseURL": self.firebase_url})
        return db.reference("/")

    def get_properties_from_db(self):
        """Get all nodes from the 'property_addresses' child, then add the value (address) from each to the 'list_of_addresses' and retun list."""
        properties_in_db = self.rtdb.child("property_addresses").get()
        list_of_addresses = [
            properties_in_db[property_id] for property_id in properties_in_db
        ]
        return list_of_addresses

    def add_property_to_db(self, property_address):
        """Add the property address argument as a new node under the 'property_addresses' child."""
        self.rtdb.child("property_addresses").push(property_address)
