from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
import pymongo
import os
from dotenv import load_dotenv

# ✅ Load environment variables from .env
load_dotenv()

# ✅ Ensure MONGO_URI is loaded correctly
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("❌ ERROR: MONGO_URI is not set correctly in .env!")

# ✅ Initialize Flask app
app = Flask(__name__)
app.config["MONGO_URI"] = MONGO_URI
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

# ✅ Initialize MongoDB
mongo = PyMongo(app)
db = mongo.db  # Assign database instance

try:
    print("✅ MongoDB connected successfully!")
    print("Collections:", db.list_collection_names())
except Exception as e:
    print("❌ MongoDB Connection Error:", e)

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    """Redirect to display all data"""
    return redirect(url_for("display_all"))

# ---------------- DISPLAY ALL DATA ---------------- #
@app.route("/displayAll")
def display_all():
    """Fetch all user data, weight tracking, and BMR data"""
    users = list(db.userInfo.find({}, {"_id": 0}))
    weight_data = list(db.weightList.find({}, {"_id": 0}))
    bmr_data = list(db.bmrList.find({}, {"_id": 0}))

    return render_template("displayAll.html", users=users, weight_data=weight_data, bmr_data=bmr_data)

# ---------------- ADD DATA ---------------- #
@app.route("/newData", methods=["GET", "POST"])
def new_data():
    """Handle new weight tracking entry"""
    if request.method == "POST":
        date = request.form.get("date", "").strip()
        weight = request.form.get("weight", "").strip()

        db.weightList.insert_one({"date": date, "weight": weight})
        flash("✅ Weight data added successfully!", "success")
        return redirect(url_for("display_all"))

    return render_template("newData.html")

# ---------------- EDIT DATA ---------------- #
@app.route("/editData/<date>", methods=["GET", "POST"])
def edit_data(date):
    """Edit an existing weight entry"""
    entry = db.weightList.find_one({"date": date}, {"_id": 0})

    if not entry:
        flash("❌ Entry not found!", "danger")
        return redirect(url_for("display_all"))

    if request.method == "POST":
        new_weight = request.form.get("weight", "").strip()
        db.weightList.update_one({"date": date}, {"$set": {"weight": new_weight}})
        flash("✅ Weight entry updated successfully!", "success")
        return redirect(url_for("display_all"))

    return render_template("editData.html", entry=entry)

# ---------------- DELETE DATA ---------------- #
@app.route("/deleteData/<date>", methods=["POST"])
def delete_data(date):
    """Delete a weight entry"""
    db.weightList.delete_one({"date": date})
    flash("✅ Weight entry deleted successfully!", "success")
    return redirect(url_for("display_all"))

# ---------------- SEARCH DATA ---------------- #
@app.route("/search", methods=["GET", "POST"])
def search():
    """Search for data by date in DDMMYYYY format"""
    result = None
    if request.method == "POST":
        date = request.form.get("date", "").strip()

        weight_result = db.weightList.find_one({"date": date}, {"_id": 0})
        bmr_result = db.bmrList.find_one({"date": date}, {"_id": 0})

        result = {"weight": weight_result, "bmr": bmr_result}
        flash("✅ Search completed!", "success")

    return render_template("search.html", result=result)

# ---------------- RUN THE FLASK APP ---------------- #
if __name__ == "__main__":
    app.run(debug=True)
