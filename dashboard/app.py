from flask import Flask, render_template, request, redirect, session
import json
import os
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = "aquila_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")

# ------------------ Helpers ------------------

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def egypt_time():
    return datetime.now(
        pytz.timezone("Africa/Cairo")
    ).strftime("%Y-%m-%d %H:%M:%S")

# ------------------ Auth ------------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/dashboard")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ------------------ Dashboard ------------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    settings = load_settings()

    return render_template(
        "dashboard.html",
        enabled=settings["enabled"],
        timeframe=settings["timeframe"],
        pairs=settings["pairs"],
        all_pairs=["EURUSD", "EURJPY", "EURGBP", "AUDCAD", "USDJPY"],
        now=egypt_time()
    )

# ------------------ Controls ------------------

@app.route("/toggle", methods=["POST"])
def toggle():
    settings = load_settings()
    settings["enabled"] = not settings["enabled"]
    save_settings(settings)
    return redirect("/dashboard")

@app.route("/save", methods=["POST"])
def save():
    settings = load_settings()
    settings["timeframe"] = request.form.get("timeframe")
    settings["pairs"] = request.form.getlist("pairs")
    save_settings(settings)
    return redirect("/dashboard")

# ------------------ Run ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
