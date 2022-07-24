# Property Finder

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img alt ="Calendar image" src="static/map.png" width="300">

## Overview

Property Finder is a Python program with the goal of helping people find their ideal property by way of customizable search paramaters. With the help of Realty Mole API, the user can draw up to 50 properties per call.

## How to Use Property Finder

### Setup

#### Settings

In order to use Property Finder, first download all necessary packages by running `requirements.txt`.

Then sign up for the plan of your choice with Realty Mole Property on rapidapi.com. There are different tiers of payment that correspond with request limits for each plan, so choose which one will best fit your needs!

Next, you will need to update the configure.json file with the following details. `api_plan` specifies which plan you choose with Realty Mole Property, the options being **basic**, **pro**, **ultra**, or **mega**. `request_frequency_per_week` specifies how many times per week the user would like to be emailed an updated list of properties that they have not yet seen. `email_server` indicates which server the user is using to send their emails. `search_params` allows users to add the desired locations they would like to recieve property listings from as a list of dictionaries. Within each location dictionary, the user can specify "city", "state", and "limit" which is the maximum number of properties to return with a cap and default of 50. `price_limit` indicates the maximum price of listings that the user would like to see. `home_type` specifies the type of property the user is interested in viewing, options being "Single Family", "Apartment", and "Condo". `min_num_beds` indicates the minimum number of beds the listings should have. `min_num_baths` indicates the minimum number of bathrooms the listings should have (can include half baths).

Below is an example of the configure.json file with specified user settings:

```json
{
  "API_plan": "basic",
  "request_frequency_per_week": 10,
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

#### Email Notifications

Next, to set up email notifications, follow the steps below:

1. Add an email address that you want property details to be sent to. You can add this address as the value for `TO_EMAIL` in the `.env` file.

2. Add the email address that will send notifications with the property details. You can add this as the value for `FROM_EMAIL` in the `.env` file. (This can be the same address as the `TO_EMAIL`, if desired).

3. Add the password for the `FROM_EMAIL` by setting the value of `EMAIL_PASSWORD` in the `.env` file.

### Running Property Finder

To run Property Finder, simply run `python3 main.py`! Property Finder will send emails with property details fitting your specifications on a schedule designed by you.

#### Attributions:

Icon made by Freepik from www.flaticon.com
