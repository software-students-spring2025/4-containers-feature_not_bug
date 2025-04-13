"""Flask application for Machine Learning Client API"""

from flask import Flask, request  # , url_for, redirect, session

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

        try:
            process_data(data)
            return "Receipt received, processed, and stored in DB", 200

        except Exception as e:  # pylint: disable=broad-exception-caught
            return (
                e,
                500,
            )

    return app


my_app = app_setup()

# keep alive
if __name__ == "__main__":
    my_app.run(
        debug=True, port=4999
    )  # running your server on development mode, setting debug to True
