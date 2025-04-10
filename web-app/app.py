"""Flask application for GoDutch - Receipt Splitter"""

# import datetime
import os
import certifi
from flask import Flask, render_template, request  # , url_for, redirect, session
# from flask_api import status

# import pymongo
# from bson.objectid import ObjectId
# import database, filter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import requests

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

    @app.route("/upload", methods=("GET", "POST"))
    def upload():
        """
        Handle form submission when receipt is uploaded
        """

        data = []
        print(request.form)
        # ensure a receipt photo was provided
        if "capture-receipt"  in request.form:
            data.append(("receipt", request.form["capture-receipt"]))
        elif "upload-receipt" in request.form:
            data.append(("receipt", request.form["upload-receipt"]))
        else: 
            return "Receipt image not found", 400
        
        # ensure all proper parameters are included
        num = int(request.form["num-people"])
        if "person-" + str(num) + "-name" not in request.form:
            return "Number of people mismatched", 400
        if "person-" + str(num+1) + "-name" in request.form:
            return "Number of people mismatched", 400
        data.append(("num-people", request.form["num-people"]))
        
        # check to ensure tip is a number (int or float) with up to 2 digits after the decimal
        try:
            s = request.form["tip"]
            tip = float(s)
        except ValueError:
            return "Tip cannot be converted into a decimal and was likely entered wrong", 400
        except: 
            return "Error in entered tip", 400
        if "." in s:
            if len(s.split(".")) != 2:
                # the tip contains more than one decimal point, or contains no digits before or after it
                return "Error in entered tip", 400
            if len(s.split(".")[1]) > 2:
                # the tip has more than two digits after the decimal point
                return "Error in entered tip", 400
        data.append(("tip", tip))

        # compile data to final form
        for i in range(0, num):
            data.append((
                "person-" + str(i+1) + "-name", request.form["person-" + str(i+1) + "-name"]
            ))
            data.append((
                "person-" + str(i+1) + "-items", request.form["person-" + str(i+1) + "-desc"]
            ))
        
        # send data
        res = requests.post(
            "http://127.0.0.1:4999/submit",
            data=data
        )
        if res.status_code == 200:
            print("received")
        else:
            return "error in sending/receiving - ensure ML client is running properly on port 4999", 400

        return render_template("upload.html", data=data)  # render home page template

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(
        debug=True
    )  # running your server on development mode, setting debug to True
