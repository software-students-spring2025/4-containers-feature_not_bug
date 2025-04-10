"""Flask application for Machine Learning Client API"""

# import datetime
import os
import certifi
from flask import Flask, request  # , url_for, redirect, session

# import pymongo
# from bson.objectid import ObjectId
# import database, filter
# requests
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

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

        data = {"receipt": "", "tip": 0, "num-people": 0, "people": []}

        # receive data from the POST request
        print(request.form)
        print(request.headers)
        print()

        # Convert data to organized form
        data["receipt"] = request.form["receipt"]
        data["num-people"] = request.form["num-people"]
        data["tip"] = request.form["tip"]
        for i in range(0, int(data["num-people"])):
            data["people"].append(
                {
                    "name": request.form["person-" + str(i + 1) + "-name"],
                    "items": request.form["person-" + str(i + 1) + "-items"],
                }
            )

        # process data .....
        print(data)
        if my_db["receipts"].find({}):
            pass

        # return confirmation of completion
        return "received", 200
        # etc

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(
        debug=True, port=4999
    )  # running your server on development mode, setting debug to True
