# Property Finder

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img alt ="Calendar image" src="static/map.png" width="300">

## Overview

Property Finder is a Python program with the goal of helping people find their ideal property using customizable search paramaters. With the help of Realty Mole API, the user can draw up to 50 properties per call, and up to 25,000 calls per month.

## How to Use Property Finder

### Setup

#### Settings

In order to use Property Finder, first download all necessary packages by running `requirements.txt`.

Then sign up for the Realty Mole Property plan of your choice on www.rapidapi.com. There are different tiers of payment with an increasing number of request limits for each plan, so choose which one will best fit your needs!

Next, you will need to update the `configure.json` file with the following details. `monthly_request_limit` specifies how many requests you would like the program to make per month. It is reccommended to made this variable less than or equal to the number of requests per month provided by your chosen Realty Mole API plan, however going above this number is completely fine as well. Just note that an additional $0.05 per call beyond your plan's allotted max will be charged. `hours_between_api_requests` specifies how much time you would like to pass before the next api call. `email_server` indicates which server the user is using to send their emails. `search_params` allows users to add the desired locations they would like to recieve property listings from as a list of dictionaries. Within each location dictionary, the user can specify "city", "state", and "limit" which is the maximum number of properties to return with a cap and default of 50. `price_limit` indicates the maximum price of listings that the user would like to see. `home_type` specifies the type of property the user is interested in viewing, options being "Single Family", "Apartment", and "Condo". `min_num_beds` indicates the minimum number of beds the listings should have. `min_num_baths` indicates the minimum number of bathrooms the listings should have (can include half baths).

Below is an example of the configure.json file with specified user settings:

```json
{
  "monthly_request_limit": 50,
  "hours_between_api_requests": 24,
  "email_server": "smtp.mail.yahoo.com",
  "search_params": [
    {
      "city": "Burlington",
      "state": "VT",
      "limit": 30
    },
    {
      "city": "Charleston",
      "state": "SC",
      "limit": 50
    }
  ],
  "price_limit": 8000000,
  "home_type": "Single Family",
  "min_num_beds": 3,
  "min_num_baths": 2.5
}
```

#### Firebase Realtime Database

Next, the Realtime Database in Firebase needs to be set up. Go to www.firebase.google.com and follow the steps to setting up a new project. If you do not already have a google account, you will need to create one. Once you have a new project go to the `Build` dropdown menu on the left side of the page, and choose `Realtime Database`. Follow the on screen instructions for creating the database.

Once your database is set up in Realtime Database, you will need to create a file called `service_account.json` containing user specific information. Below is an example of what the file should look like:

```json
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```

#### Email Notifications

Finally, to set up email notifications, follow the steps below:

1. Add an email address that you want property details to be sent to. You can add this address as the value for `TO_EMAIL` in the `.env` file.

2. Add the email address that will send notifications with the property details. You can add this as the value for `FROM_EMAIL` in the `.env` file. (This can be the same address as the `TO_EMAIL`, if desired).

3. Add the password for the `FROM_EMAIL` by setting the value of `EMAIL_PASSWORD` in the `.env` file.

### Running Property Finder

To run Property Finder, simply run `python3 main.py`! Property Finder will send emails with property details fitting your specifications on a schedule designed by you. Even if there are no new properties or you have run out of API calls for the month, Property Finder will send you an email notification. Happy house hunting!

#### Attributions:

Icon made by Freepik from www.flaticon.com
