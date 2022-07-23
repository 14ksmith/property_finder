# Property Finder

&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<img alt ="Calendar image" src="static/map.png" width="300">

## Overview

Property Finder is a Python program with the goal of helping people find their ideal property with ease.

## How to Use Property Finder

### Setup

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
      "limit": 30
    }
  ],
  "price_limit": 8000000,
  "home_type": "Single Family",
  "min_num_beds": 3,
  "min_num_baths": 2.5
}
```

### Running Property Finder

To run Property Finder, simply run `python3 main.py`.

#### Attributions:

Icon made by Freepik from www.flaticon.com
