# Web App - team Web Crawlers

# import modules that are necessary for this program
import pymongo
import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response
import pymongo.mongo_client

# instantiate a flask-based web app
app = Flask(__name__)

# make connection to the database
connection = pymongo.MongoClient("mongodb+srv://lgl1876523678:1017@cluster0.k8xwe.mongodb.net/?retryWrites=true&w=majority")
db = connection['project2_db']

# flask route
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('newUser.html')

@app.route('/displayAll')
def displayAll():
    return render_template('displayAll.html')
