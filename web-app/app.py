"""Flask application for GoDutch - Receipt Splitter"""

# import datetime
import os
import certifi
from flask import Flask, render_template, request, session, redirect, url_for

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
    dbname = os.getenv(
        "MONGO_DB", "dutch_pay"
    )  # Changed default to actual database name
    my_db = client[dbname]

    app = Flask(__name__, static_folder="static")
    app.secret_key = os.getenv("SECRET_KEY", "godutch-development-key")

    # Ensure the static folders exist
    os.makedirs(os.path.join(app.static_folder, "uploads"), exist_ok=True)

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
        if "capture-receipt" in request.form:
            data.append(("receipt", request.form["capture-receipt"]))
        elif "upload-receipt" in request.form:
            data.append(("receipt", request.form["upload-receipt"]))
        else:
            return "Receipt image not found", 400


        num = int(request.form["num-people"])
        if (
            "person-" + str(num) + "-name" not in request.form
            or "person-" + str(num + 1) + "-name" in request.form
        ):
            return "Number of people mismatched", 400
        data.append(("num-people", request.form["num-people"]))

        try:
            s = request.form["tip"]
            tip = float(s)
        except ValueError:
            return (
                "Tip cannot be converted into a decimal and was likely entered wrong",
                400,
            )
        if "." in s:
            if len(s.split(".")) != 2 or len(s.split(".")[1]) > 2:
                return "Error in entered tip", 400
        data.append(("tip", tip))

        for i in range(0, num):
            data.append(
                (
                    "person-" + str(i + 1) + "-name",
                    request.form["person-" + str(i + 1) + "-name"],
                )
            )
            data.append(
                (
                    "person-" + str(i + 1) + "-items",
                    request.form["person-" + str(i + 1) + "-desc"],
                )
            )
        try:
            res = requests.post("http://127.0.0.1:4999/submit", data=data, timeout=60)
            if res.status_code == 200:
                print("received successful response from ML client")
                result_data = res.json()
                session["result_id"] = result_data.get("result_id")
                return redirect(url_for("result"))
            else:
                return (
                    f"Error processing receipt: {res.text}",
                    400,
                )
        except requests.RequestException as e:
            return (
                "Error connecting to ML client - ensure ML client is running properly on port 4999: "
                + str(e),
                400,
            )

        return render_template("upload.html") 

    @app.route("/result", methods=["GET"])
    def result():
        """
        Display results of data analysis
        """
        result_id = session.get("result_id")
        result_data = None

        if result_id:
            try:
                res = requests.get(
                    f"http://127.0.0.1:4999/results/{result_id}", timeout=10
                )
                if res.status_code == 200:
                    result_data = res.json()
                else:
                    print(f"Error fetching results: {res.text}")
            except requests.RequestException as e:
                print(f"Error connecting to ML client: {str(e)}")

        return render_template("result.html", result_data=result_data)

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(debug=True)
