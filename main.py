from dotenv import load_dotenv
import os
from database import Firebase
from property_results import (
    email_formatted_property_results,
    get_filtered_property_results,
)


# load environment variables from .env
load_dotenv()


firebase = Firebase(
    os.getenv("FIREBASE_RTDB_URL"), os.getenv("PATH_TO_FIREBASE_SERVICE_ACCOUNT")
)

# ==========================================================
# example firebase usage
# ==========================================================

## SET
## Sets the data at this location to a given value. If you already have values and children created, they will be overridden
# This will set a value directly at the route
firebase.rtdb.set("seeds")

## CHILD
## Returns a reference to the specified child node
# This will create a new child called "watermelon" if there is not one already, and set the value to 'seeds'
# If there is already a child called "watermelon", it will override that child with the new once, replacing it
input("press enter when ready\n")
firebase.rtdb.child("watermelon").set({"watermelon": "seeds"})

# This will override the old "watermelon" child, and set the value to 'rind'
input("press enter when ready\n")
firebase.rtdb.child("watermelon").set("rind")

# This will make multiple children off the same node
input("press enter when ready\n")
firebase.rtdb.child("watermelon").child("big").set("huge")

# Change this back to original configuration
input("press enter when ready\n")
firebase.rtdb.child("watermelon").set({"watermelon": "seeds"})


## PUSH
##ALWAYS MAKES A NEW CHILD NODE
# Creates a new child node. Optional value argument can be used to provide an ititial value fo rhte child node,
#       otherwise the new child will have an empty string as the default value
# This will create a new child node with an empty string as the value
input("press enter when ready\n")
firebase.rtdb.push("")
# This will create a new child node with "watermelon" as the value
input("press enter when ready\n")
firebase.rtdb.push("watermelon")
# If a key is indicated with the value, then it will create the child with the specified key: value pair
input("press enter when ready\n")
firebase.rtdb.push({"watermelon": "seeds", "apple": "core", "grape": "skin"})
# this will just create another child node with the following dictionary key:value pairs
input("press enter when ready\n")
firebase.rtdb.push({"watermelon": "rind", "apple": "seeds", "grape": "fruit"})


## UPDATE
# Updates the specified child keys of this reference to the provided values.
# Needs dict. of child keys to update and their new values
# Same as 'patch'
firebase.rtdb.child("watermelon").update({"watermelon": "smoothie"})

## GET
# Returns the value at the current location of the database
# This will return the value at the child named "watermelon"
input("press enter when ready\n")
print(firebase.rtdb.child("watermelon").get())


## DELETE
# This deletes the specified value or child
input("press enter when ready\n")
firebase.rtdb.child("watermelon").delete()


# ==========================================================
# ==========================================================

# # Return the filtered property results and set to filtered_property_results
# filtered_property_results = get_filtered_property_results()

# # Email the filtered property results
# email_formatted_property_results(filtered_property_results=filtered_property_results)
