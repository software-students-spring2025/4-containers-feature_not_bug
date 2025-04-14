"""Flask application for Machine Learning Client API"""

from flask import Flask, request, jsonify  # , url_for, redirect, session

from analyzer import process_data


def app_setup():
    """setup the app"""
    app = Flask(__name__, static_folder="assets")

    @app.route("/", methods=["GET"])
    def show():
        """
        Sanity check to check in browser if endpoint is functional
        """
        return "running", 200

    @app.route("/submit", methods=["POST"])
    def submit():
        """
        Receive data from the web-app and run analysis
        """
        print("reached /submit")
        print("ML Client: request.form contents:", request.form)
        print("ML Client: request.files contents:", request.files)

        data = {"receipt": "", "tip": 0, "num-people": 0, "people": []}

        # receive data from the POST request

        # Convert data to organized form
        # data["receipt"] = request.form["receipt"]
        data["num-people"] = request.form["num-people"]
        data["tip"] = request.form["tip"]
        for i in range(0, int(data["num-people"])):
            data["people"].append(
                {
                    "name": request.form["person-" + str(i + 1) + "-name"],
                    "items": request.form["person-" + str(i + 1) + "-items"],
                }
            )

        if "receipt" not in request.files:
            return jsonify({"error": "No receipt file provided"}), 400
        receipt_file = request.files["receipt"]
        print("ML Client: Received receipt file with filename:", receipt_file.filename)

        try:
            result_id = process_data(data, receipt_file)
            print("ML Client processed data:", result_id)
            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Receipt received, processed, and stored in DB",
                        "result_id": str(result_id)
                    }
                ),
                200,
            )

        except Exception as e:  # pylint: disable=broad-exception-caught
            print("Exception caught:", e)
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Error processing the receipt in the ML client API",
                        "error": str(e),
                    }
                ),
                500,
            )

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(
        debug=True, port=4999
    )  # running your server on development mode, setting debug to True
