"""Flask application for GoDutch - Receipt Splitter"""

import os
import certifi
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import requests
from bson.objectid import ObjectId

load_dotenv()


def app_setup():
    """setup the app"""
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri, server_api=ServerApi("1"), tlsCAFile=certifi.where())
    dbname = os.getenv("MONGO_DB", "dutch_pay")
    app = Flask(__name__, static_folder="static")
    app.secret_key = os.getenv("SECRET_KEY", "godutch-development-key")

    os.makedirs(os.path.join(app.static_folder, "uploads"), exist_ok=True)

    # Get DB connection
    db = client[dbname]

    @app.route("/", methods=("GET", "POST"))
    def show_dashboard():
        """
        Show homepage / dashboard
        """

        data = {}
        if request.method == "GET":
            data = {"filler": "filler"}

        return render_template("index.html", data=data)

    @app.route("/upload", methods=("GET", "POST"))
    def upload():
        """
        Handle form submission when receipt is uploaded
        """

        data = []
        print(request.form)

        if (
            "capture-receipt" not in request.form
            and "upload-receipt" not in request.form
        ):
            return "Receipt image not found", 400

        if "capture-receipt" in request.form and request.form["capture-receipt"] != "":
            data.append(("receipt", request.form["capture-receipt"]))
        elif "upload-receipt" in request.form and request.form["upload-receipt"] != "":
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
            tip_str = request.form["tip"]
            tip = float(tip_str)
        except ValueError:
            return (
                "Tip cannot be converted into a decimal and was likely entered wrong",
                400,
            )
        if "." in tip_str:
            if len(tip_str.split(".")) != 2 or len(tip_str.split(".")[1]) > 2:
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
            res = requests.post("http://127.0.0.1:5000/submit", data=data, timeout=60)
            if res.status_code == 200:
                print("received successful response from ML client")
                # Store the result ID in session
                result_data = res.json()
                session["result_id"] = result_data.get("result_id")
                # Redirect to results page
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

        if not result_id:
            return ("No result_id found in session", 400)

        result_data = db.receipts.find_one(
            {"_id": ObjectId(result_id), "charge_info": {"$exists": True}}
        )
        if not result_data:
            return ("No results found", 404)

        return render_template("result.html", result_data=result_data)

    return app


my_app = app_setup()

if __name__ == "__main__":
    my_app.run(debug=True)
