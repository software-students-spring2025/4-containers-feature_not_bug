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

    # Store db reference but not using it yet
    # my_db = client[dbname]  # Commented out to avoid unused variable warning

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
        # ensure a receipt photo was provided
        if (
            "capture-receipt" not in request.form
            and "upload-receipt" not in request.form
        ):
            return "Receipt image not found", 400

        if "capture-receipt" in request.form:
            data.append(("receipt", request.form["capture-receipt"]))
        elif "upload-receipt" in request.form:
            data.append(("receipt", request.form["upload-receipt"]))

        # ensure all proper parameters are included
        num = int(request.form["num-people"])
        if (
            "person-" + str(num) + "-name" not in request.form
            or "person-" + str(num + 1) + "-name" in request.form
        ):
            return "Number of people mismatched", 400
        data.append(("num-people", request.form["num-people"]))

        # check to ensure tip is a number (int or float) with up to 2 digits after the decimal
        try:
            tip_str = request.form["tip"]
            tip = float(tip_str)
        except ValueError:
            return (
                "Tip cannot be converted into a decimal and was likely entered wrong",
                400,
            )
        if "." in tip_str:
            if len(tip_str.split(".")) != 2 or len(tip_str.split(".")[1]) > 2:
                # the tip contains more than one decimal point,
                # or contains no digits before or after it,
                # or has more than two digits after the decimal point
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

            return (
                f"Error processing receipt: {res.text}",
                400,
            )
        except requests.RequestException as req_error:
            error_msg = "Error connecting to ML client - ensure ML client is running "
            error_msg += f"properly on port 4999: {str(req_error)}"
            return (
                error_msg,
                400,
            )


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
            except requests.RequestException as req_error:
                print(f"Error connecting to ML client: {str(req_error)}")

        return render_template("result.html", result_data=result_data)

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(debug=True)
