"""Flask application for Machine Learning Client API"""

# import datetime
import os
import certifi
from flask import Flask, request  # , url_for, redirect, session

# import pymongo
# from bson.objectid import ObjectId
# import database, filter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import requests
#from flask_api import status

# load environment variables
load_dotenv()


def app_setup():
    """setup the app"""
    # connect MongoDB
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    dbname = os.getenv("MONGO_DBNAME")
    my_db = client[dbname]

    app = Flask(__name__, static_folder="assets")

    @app.route("/", methods=["GET"])
    def show():
        return "running", 200

    @app.route("/submit", methods=["POST"])
    def submit():
        """
        Submit a receipt and other data to the API endpoint
        """
        print("reached /submit")
        # receive data from the POST request
        data = request.data
        # manipulate data ...
        if data:
            pass
        # store data in database
        if my_db:
            pass
        # etc

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(
        debug=True, 
        port=4999
    )  # running your server on development mode, setting debug to True
