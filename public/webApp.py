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
    age = float(request.form['age'])  
    height = float(request.form['height'])
    sex = request.form['sex'].lower()
    tweight = float(request.form['target'])

    info = {
        'name': username,
        'password': password,
        'age': age,
        'height': height,
        'sex': sex,
        'target': tweight
    }
    db['userInfo'].insert_one(info)
    user = db['userInfo'].find_one({'name': username})
    session['user_id'] = str(user['_id'])
    return redirect(url_for('displayAll'))

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/handleSearch', methods=['GET', 'POST'])
def handleSearch():
    if request.method == 'POST':
        day = request.form.get('day')
        month = request.form.get('month')
        year = request.form.get('year')
    else:
        day = request.args.get('day')
        month = request.args.get('month')
        year = request.args.get('year')

    if not day or not month or not year:
        return render_template('search.html', error="Please provide all fields")

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

    day = int(request.form['day'])
    month = int(request.form['month'])
    year = int(request.form['year'])
    weight = float(request.form['weight'])

    db['weightList'].insert_one({
        'name': user['name'],
        'day': day,
        'month': month,
        'year': year,
        'weight': weight
    })
    return redirect(url_for('displayAll'))

@app.route('/newGoal')
def newGoal():
    return render_template('newGoals.html')

@app.route('/handleNewGoal', methods=['POST'])
def handleNewGoal():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db['userInfo'].find_one({'_id': ObjectId(session['user_id'])})
    new_target = float(request.form['calorie'])

    db['userInfo'].update_one(
        {'_id': ObjectId(session['user_id'])},
        {'$set': {'target': new_target}}
    )

    return redirect(url_for('displayAll'))

@app.route('/displayAll')
def displayAll():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db['userInfo'].find_one({'_id': ObjectId(session['user_id'])})
    weight_list = list(db['weightList'].find({'name': user['name']}))

    body_data = []
    for doc in weight_list:
        body_data.append({
            '_id': str(doc['_id']),  # Convert ObjectId to string for HTML
            'day': doc.get('day', 'N/A'),
            'month': doc.get('month', 'N/A'),
            'year': doc.get('year', 'N/A'),
            'weight': doc.get('weight', 'N/A')
        })

    return render_template('displayAll.html', body_data=body_data)

# New route: Edit data
@app.route('/editData/<entry_id>', methods=['GET', 'POST'])
def editData(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    entry = db['weightList'].find_one({'_id': ObjectId(entry_id)})
    
    if request.method == 'POST':
        new_weight = float(request.form['weight'])
        db['weightList'].update_one(
            {'_id': ObjectId(entry_id)},
            {'$set': {'weight': new_weight}}
        )
        return redirect(url_for('displayAll'))
    
    return render_template('editData.html', entry=entry)

# New route: Delete data
@app.route('/deleteData/<entry_id>', methods=['POST'])
def deleteData(entry_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db['weightList'].delete_one({'_id': ObjectId(entry_id)})
    return redirect(url_for('displayAll'))

if __name__ == "__main__":
    app.run(debug=True)
