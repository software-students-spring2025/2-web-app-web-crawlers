import pymongo
import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
connection = pymongo.MongoClient(mongo_uri)
db = connection['project2_db']

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user_collection = db['userInfo']
        result = user_collection.find_one({'name': username})
        if not result or 'password' not in result:
            return render_template('login.html', error="User not found")
        if result['password'] == password:
            session['user_id'] = str(result['_id'])
            return redirect(url_for('displayAll'))
        return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('newUser.html')

@app.route('/handleRegister', methods=['POST'])
def handleRegister():
    username = request.form['username']
    password = request.form['password']
    age = request.form['age']
    height = request.form['height']
    sex = request.form['sex']
    tweight = request.form['target']

    information = {
        'name': username,
        'password': password,
        'age': age,
        'height': height,
        'sex': sex,
        'target': tweight
    }
    db['userInfo'].insert_one(information)
    
    user = db['userInfo'].find_one({'name': username})
    session['user_id'] = str(user['_id'])
    
    return redirect(url_for('displayAll'))


@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/handleSearch', methods=['POST'])
def handleSearch():
    day = request.form['day']
    month = request.form['month']
    year = request.form['year']
    docs = db['weightList'].find_one({
        'day': int(day),
        'month': int(month),
        'year': int(year)
    })
    return render_template('search.html', info=docs)

@app.route('/newData')
def newData():
    return render_template('newData.html')

@app.route('/handleNewData', methods=['POST'])
def handleNewData():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = db['userInfo'].find_one({'_id': ObjectId(session['user_id'])})
    now = datetime.datetime.utcnow()
    day, month, year = now.day, now.month, now.year
    weight = request.form['weight']
    information = {
        'name': user['name'],
        'day': day,
        'month': month,
        'year': year,
        'weight': weight
    }
    db['weightList'].insert_one(information)
    return redirect(url_for('displayAll'))

@app.route('/newGoal')
def newGoal():
    return render_template('newGoals.html')

@app.route('/handleNewGoal', methods=['POST'])
def handleNewGoal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    target_weight = request.form['weight']
    db['userInfo'].update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$set': {'target': target_weight}}
    )
    return redirect(url_for('displayAll'))

@app.route('/displayAll')
def displayAll():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db['userInfo'].find_one({'_id': ObjectId(session['user_id'])})

    # BMR
    bmr_list = list(db['bmrList'].find({'name': user['name']}))
    bmr_dict = {
        (doc['day'], doc['month'], doc['year']): doc
        for doc in bmr_list
    }

    # Weight
    weight_list = list(db['weightList'].find({'name': user['name']}))
    weight_dict = {
        (doc['day'], doc['month'], doc['year']): doc
        for doc in weight_list
    }

    # Get *all* date tuples from both sets
    all_dates = set(bmr_dict.keys()) | set(weight_dict.keys())

    body_data = []

    # Sort by (year, month, day) if you want chronological order
    for date_key in sorted(all_dates, key=lambda x: (x[2], x[1], x[0])):
        bmr_record = bmr_dict.get(date_key, {})
        weight_record = weight_dict.get(date_key, {})

        day_val, month_val, year_val = date_key
        current_day = {
            'day': day_val,
            'month': month_val,
            'year': year_val,
            'weight': weight_record.get('weight', 'N/A'),
            'bmr': bmr_record.get('bmr', 'N/A'),
            'calorie': bmr_record.get('calorie', 'N/A')
        }
        body_data.append(current_day)

    return render_template('displayAll.html', body_data=body_data)

if __name__ == "__main__":
    app.run(debug=True)
