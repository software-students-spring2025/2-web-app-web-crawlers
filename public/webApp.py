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
    age = float(request.form['age'])  # cast to float (or int if you prefer strictly int)
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
    print("DEBUG: user document =", user)  # see what's stored in user

    # Force everything to numeric
    day = int(request.form['day'])
    month = int(request.form['month'])
    year = int(request.form['year'])
    weight = float(request.form['weight'])
    user_age = float(user['age'])       # forcibly cast in case it’s str
    user_height = float(user['height']) # forcibly cast in case it’s str
    user_target = float(user['target']) # forcibly cast in case it’s str

    db['weightList'].insert_one({
        'name': user['name'],
        'day': day,
        'month': month,
        'year': year,
        'weight': weight
    })

    if user['sex'] == 'male':
        bmr_val = 10 * weight + 6.25 * user_height - 2 * user_age + 5
    else:
        bmr_val = 10 * weight + 6.25 * user_height - 2 * user_age - 161

    gap_val = user_target - bmr_val

    print("DEBUG: BMR =", bmr_val, "gap =", gap_val)  # debug prints

    db['bmrList'].insert_one({
        'name': user['name'],
        'day': day,
        'month': month,
        'year': year,
        'bmr': bmr_val,
        'calorie_gap': gap_val
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

    bmr_records = db['bmrList'].find({'name': user['name']})
    for record in bmr_records:
        bmr_val = float(record.get('bmr', 0))
        updated_gap = new_target - bmr_val
        db['bmrList'].update_one(
            {'_id': record['_id']},
            {'$set': {'calorie_gap': updated_gap}}
        )
    return redirect(url_for('displayAll'))

@app.route('/displayAll')
def displayAll():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db['userInfo'].find_one({'_id': ObjectId(session['user_id'])})
    bmr_list = list(db['bmrList'].find({'name': user['name']}))
    weight_list = list(db['weightList'].find({'name': user['name']}))

    bmr_dict = {}
    for doc in bmr_list:
        # Convert doc day/month/year to int in case there's a leftover string
        dk = (int(doc['day']), int(doc['month']), int(doc['year']))
        bmr_dict[dk] = doc

    weight_dict = {}
    for doc in weight_list:
        dk = (int(doc['day']), int(doc['month']), int(doc['year']))
        weight_dict[dk] = doc

    all_dates = set(bmr_dict.keys()) | set(weight_dict.keys())
    print("DEBUG: all_dates =", all_dates)

    body_data = []

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
            'calorie_gap': bmr_record.get('calorie_gap', 'N/A')
        }
        body_data.append(current_day)

    return render_template('displayAll.html', body_data=body_data)

if __name__ == "__main__":
    app.run(debug=True)
