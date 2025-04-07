from flask import Flask, render_template, request, url_for, redirect, session
#import pymongo
from bson.objectid import ObjectId
import database, filter
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi
from dotenv import load_dotenv
from flask_session import Session
import datetime

'''
notes / instructions

run app.py, then go to 127.0.0.1:5000 in browser

'''

# load environment variables 
load_dotenv()
'''
# connect MongoDB
uri = os.getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
Mongo_DBNAME= os.getenv("MONGO_DBNAME")
myDb= client[Mongo_DBNAME]
'''

app = Flask(__name__, static_folder='assets')

# start new user session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# homepage / dashboard
@app.route("/", methods=('GET', 'POST'))
def show_dashboard():
    
    # show the dashboard
    if request.method == "GET":              
        
        # get all necessary data
        data = {
            
        }
    elif request.method == "POST":
        pass 

    return render_template('index.html') # render home page template 

