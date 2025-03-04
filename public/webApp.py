from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

# Initialize MongoDB
mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def home():
    """Redirect to login if not authenticated"""
    if "user_id" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("display_all"))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Allow user to log in with any username/password"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Store the username in session to track login status
        session["user_id"] = username
        flash("Login successful!", "success")
        return redirect(url_for("display_all"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    """Handle user logout"""
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/displayAll")
def display_all():
    """Restrict access to logged-in users"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    users = []
    weight_data = list(db.weightList.find({}, {"_id": 0}))
    bmr_data = list(db.bmrList.find({}, {"_id": 0}))

    return render_template("displayAll.html", users=users, weight_data=weight_data, bmr_data=bmr_data)

@app.route("/newData", methods=["GET", "POST"])
def new_data():
    """Handle new weight tracking entry"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        date = request.form["date"]
        weight = request.form["weight"]
        db.weightList.insert_one({"date": date, "weight": weight})
        flash("Weight data added successfully!", "success")
        return redirect(url_for("display_all"))

    return render_template("newData.html")

@app.route("/editData/<date>", methods=["GET", "POST"])
def edit_data(date):
    """Edit an existing weight entry"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    entry = db.weightList.find_one({"date": date}, {"_id": 0})

    if not entry:
        flash("Entry not found!", "danger")
        return redirect(url_for("display_all"))

    if request.method == "POST":
        new_weight = request.form["weight"]
        db.weightList.update_one({"date": date}, {"$set": {"weight": new_weight}})
        flash("Weight entry updated successfully!", "success")
        return redirect(url_for("display_all"))

    return render_template("editData.html", entry=entry)

@app.route("/deleteData/<date>", methods=["POST"])
def delete_data(date):
    """Delete a weight entry"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    db.weightList.delete_one({"date": date})
    flash("Weight entry deleted successfully!", "success")
    return redirect(url_for("display_all"))

@app.route("/search", methods=["GET", "POST"])
def search():
    """Search for data by date in DDMMYYYY format"""
    if "user_id" not in session:
        return redirect(url_for("login"))

    result = None
    if request.method == "POST":
        date = request.form["date"]
        weight_result = db.weightList.find_one({"date": date}, {"_id": 0})
        bmr_result = db.bmrList.find_one({"date": date}, {"_id": 0})
        result = {"weight": weight_result, "bmr": bmr_result}
        flash("Search completed!", "success")

    return render_template("search.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
