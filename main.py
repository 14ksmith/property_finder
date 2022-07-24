from dotenv import load_dotenv
from property_results import get_filtered_property_results
from send_email import send_email

# load environment variables from .env
load_dotenv()

# TODO: check 'lastSeen' date for each address returned in the search and if it is equal to current date, then send it in an email
#           *if it is not equal to the current date, that means it has already been seen by the user so it is not new
