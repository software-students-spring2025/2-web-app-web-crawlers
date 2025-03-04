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

current_user = ''


@app.route('/')
def login():
    global current_user  

    if request.method == 'POST':  
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user_collection = db['userInfo']
        result = user_collection.find_one({'name': username})

        if not result or 'password' not in result:
            return render_template('login.html', error="User not found")

        if result['password'] == password:
            current_user = user_collection.find_one({'name':username}) 
            return render_template('displayAll.html')

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html') 



@app.route('/register')
def register():
    return render_template('newUser.html')

@app.route('/handleRegister', methods=['POST'])
def handleRegister():
    global current_user
    # store new user info in the database
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    height = request.form['height']
    sex = request.form['sex']
    tweight = request.form['weight']
    information = {
        'name':username,
        'password':password,
        'age':age,
        'height':height,
        'sex':sex,
        'target':tweight,
    }
    mongoid = db['userInfo'].insert_one(information)
    current_user = db['userInfo'].find_one({'name': username})

    # redirect to displayAll page
    return redirect(url_for('displayAll'))

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/handleSearch')
def handleSearch():
    # process the search conditions
    day = request.form['day']
    month = request.form['month']
    year = request.form['year']
    docs = db.weightList.find({
        'day':day,
        'month':month,
        'year':year,
    })
        
    # redirect to displayAll page with conditions
    return redirect(url_for('search'), info=docs)

@app.route('/newData')
def newData():

    return render_template('newData.html')

@app.route('/handleNewData', methods=['POST'])
def handleNewData():
    # process the new data
    time = datetime.utcnow()
    day = time.day
    month = time.month
    year = time.month
    weight = request.form['weight']
    information = {
        'name':current_user,
        'day':day,
        'month':month,
        'year':year,
        'weight':weight
    }
    mongoid = db.weightList.insert_one(information)
    
    # redirect to displayAll page with new data
    return redirect(url_for('displayAll'))

@app.route('/newGoal')
def newGoal():
    
    return render_template('newGoals.html')

@app.route('/handleNewGoal', methods=['POST'])
def handleNewGoal():
    # process the new goal
    target_weight = request.form['weight']
    db.userInfo.update_one({
        {'name': current_user},
        {
            '$set':{
                'target':target_weight
            }
        }
    })
    # redirect to displayAll page with new goal
    return redirect(url_for('displayAll'))

@app.route('/displayAll')
def displayAll():
    global current_user
    if not current_user:
        return redirect(url_for('login'))  

    body_data = []
    current_user_name = current_user['name']
    bmrdb = list(db['bmrList'].find({'name': current_user_name}))
    weightdb = {
        (entry['day'], entry['month'], entry['year']): entry
        for entry in db['weightList'].find({'name': current_user_name})
    }

    for day in bmrdb:
        date_key = (day['day'], day['month'], day['year'])

        current_day = {
            'day': day['day'],
            'month': day['month'],
            'year': day['year'],
            'weight': day['weight'],
            'bmr': weightdb.get(date_key, {}).get('bmr', 'N/A'),
            'calorie': weightdb.get(date_key, {}).get('calorie', 'N/A')
        }

        body_data.append(current_day)

    return render_template('displayAll.html', body_data=body_data)

app.run()