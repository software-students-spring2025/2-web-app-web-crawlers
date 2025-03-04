from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
import pymongo  # ✅ ADDED THIS IMPORT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")

try:
    client = pymongo.MongoClient(MONGO_URI)
    db = client["project2_db"]  # Ensure this matches the database name in MongoDB
    print(" MongoDB connected successfully!")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print(" MongoDB Connection Error:", e)
# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    """Redirect to display all data"""
    return redirect(url_for("display_all"))

# ---------------- USER REGISTRATION ---------------- #
@app.route("/newUser", methods=["GET", "POST"])
def new_user():
    """Handle user registration"""
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]  # TODO: Hash passwords in production
        age = request.form["age"]
        height = request.form["height"]
        sex = request.form["sex"]

        # Check if user already exists
        if db.userInfo.find_one({"name": name}):
            flash("❌ Username already exists!", "danger")
            return redirect(url_for("new_user"))

        db.userInfo.insert_one({"name": name, "password": password, "age": age, "height": height, "sex": sex})
        flash("✅ Account created! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("newUser.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        user = db.userInfo.find_one({"name": name})

        if user and user["password"] == password:  # TODO: Use hashed passwords
            flash("✅ Login successful!", "success")
            return redirect(url_for("display_all"))
        else:
            flash("❌ Invalid username or password!", "danger")
            return render_template("login.html", error="Invalid username or password!")

    return render_template("login.html")

# ---------------- WEIGHT TRACKER ---------------- #
@app.route("/newData", methods=["GET", "POST"])
def new_data():
    """Handle new weight tracking entry"""
    if request.method == "POST":
        date = request.form["date"]
        weight = request.form["weight"]

        db.weightList.insert_one({"date": date, "weight": weight})
        flash("✅ Weight data added successfully!", "success")
        return redirect(url_for("display_all"))

    return render_template("newData.html")

# ---------------- BMR TRACKER ---------------- #
@app.route("/newGoals", methods=["GET", "POST"])
def new_goals():
    """Handle new BMR entry"""
    if request.method == "POST":
        date = request.form["date"]
        calorie = request.form["calorie"]
        bmr = request.form["bmr"]  # Optional: Calculate dynamically

        db.bmrList.insert_one({"date": date, "calorie": calorie, "bmr": bmr})
        flash("✅ BMR data added successfully!", "success")
        return redirect(url_for("display_all"))

    return render_template("newGoals.html")

# ---------------- DISPLAY ALL DATA ---------------- #
@app.route("/displayAll")
def display_all():
    """Fetch all user data, weight tracking, and BMR data"""
    users = list(db.userInfo.find({}, {"_id": 0}))
    weight_data = list(db.weightList.find({}, {"_id": 0}))
    bmr_data = list(db.bmrList.find({}, {"_id": 0}))

    return render_template("displayAll.html", users=users, weight_data=weight_data, bmr_data=bmr_data)

# ---------------- SEARCH DATA ---------------- #
@app.route("/search", methods=["GET", "POST"])
def search():
    """Search for data by date"""
    result = None
    if request.method == "POST":
        date = request.form["date"]
        
        weight_result = db.weightList.find_one({"date": date}, {"_id": 0})
        bmr_result = db.bmrList.find_one({"date": date}, {"_id": 0})

        if weight_result or bmr_result:
            result = {"weight": weight_result, "bmr": bmr_result}
            flash("✅ Data found!", "success")
        else:
            flash("❌ No data found for this date.", "danger")

    return render_template("search.html", result=result)

# ---------------- RUN THE FLASK APP ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
