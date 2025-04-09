"""Flask application for GoDutch - Receipt Splitter"""

# import datetime
import os
import certifi
from flask import Flask, render_template, request  # , url_for, redirect, session

# import pymongo
# from bson.objectid import ObjectId
# import database, filter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv


# load environment variables
load_dotenv()


def app_setup():

    # connect MongoDB
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    Mongo_DBNAME = os.getenv("MONGO_DBNAME")
    myDb = client[Mongo_DBNAME]

    app = Flask(__name__, static_folder="assets")

    @app.route("/", methods=("GET", "POST"))
    def show_dashboard():
        """
        Show homepage / dashboard
        """

        data = {}
        # show the dashboard
        if request.method == "GET":
            # get all necessary data
            data = {"filler": "filler"}

        return render_template("index.html", data=data)  # render home page template

    return app


app = app_setup()

# keep alive
if __name__ == "__main__":
    app.run(
        debug=True
    )  # running your server on development mode, setting debug to True
