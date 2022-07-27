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


print(firebase.rtdb.child("watermelon").get())
firebase.rtdb.child("watermelon").delete()


input("press enter when ready\n")
# equivalent to put, it overwrites the key and the value at the key.
# if there is no key, it will make the key there
firebase.rtdb.push("watermelon")

# you can also add dictionaries, lists, numbers, strings and any other type that can be serialized into json
firebase.rtdb.push({"key_here": "valHere"})


firebase.rtdb.update()

# input("press enter when ready\n")

# lets add a child
# firebase.rtdb.child("watermelon").push("seeds")


firebase.rtdb.child("watermelon").child("big").set("seeds")

# now this will overwrite the value at big
firebase.rtdb.child("watermelon").child("big").set("rind")

input("press enter when ready\n")
# gets the node at the reference
# note that this is not getting the data at the node
# also note that you can chain children nodes
firebase.rtdb.child("")

input("press enter when ready\n")
# now we will overwrite some data
firebase.rtdb.push("")

input("press enter when ready\n")
# now we will get the data and print it
firebase.rtdb.child("").get()

input("press enter when ready\n")
firebase.rtdb.get("watermelon")

input("press enter when ready\n")
firebase.rtdb.delete()

# ==========================================================
# ==========================================================

# # Return the filtered property results and set to filtered_property_results
# filtered_property_results = get_filtered_property_results()

# # Email the filtered property results
# email_formatted_property_results(filtered_property_results=filtered_property_results)
