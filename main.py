from dotenv import load_dotenv
from property_finder.property_finder import find_properties
import asyncio
from aiohttp import ClientSession


if __name__ == "__main__":
    # load environment variables from .env
    load_dotenv()

    # find properties and write the new listings to the database as well as send an email notification containing the details
    find_properties()
