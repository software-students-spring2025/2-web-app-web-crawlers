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
@app.route('/')
def login():

    return render_template('login.html')

@app.route('/register')
def register():

    return render_template('newUser.html')

@app.route('/handleRegister', methods=['POST'])
def handleRegister():
    # store new user info in the database

    # redirect to displayAll page
    return redirect(url_for('displayAll'))

@app.route('/search')
def search():

    return render_template('search.html')

@app.route('/handleSearch')
def handleSearch():
    # process the search conditions

    # redirect to displayAll page with conditions
    return redirect(url_for('displayAll'))

@app.route('/newData')
def newData():

    return render_template('newData.html')

@app.route('/handleNewData', methods=['POST'])
def handleNewData():
    # process the new data

    # redirect to displayAll page with new data
    return redirect(url_for('displayAll'))

@app.route('/newGoal')
def newGoal():
    
    return render_template('newGoal.html')

@app.route('/handleNewGoal', methods=['POST'])
def handleNewGoal():
    # process the new goal

    # redirect to displayAll page with new goal
    return redirect(url_for('displayAll'))

@app.route('/displayAll')
def displayAll():
    # check for search condition
    # if no search condition, display all data
    # if there is condition, filter the results

    # redirect to displayAll page
    return render_template('displayAll.html')

app.run()