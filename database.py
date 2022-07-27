from firebase_admin import initialize_app, credentials, db


class Firebase:
    def __init__(self, firebase_url, path_to_service_account):
        self.firebase_url = firebase_url
        self.path_to_service_account = path_to_service_account
        self.rtdb = self.initialize_connection()

    def initialize_connection(self):
        # initialize connection through a service account
        cred = credentials.Certificate(self.path_to_service_account)
        initialize_app(cred, {"databaseURL": self.firebase_url})
        return db.reference("/")
