import json

def initialize_settings():
    """Open configure.json and return the settings as a dictionary."""
    with open ("configure.json") as config:
        return json.load(config)