from flask import Flask, render_template, redirect, url_for, session, request
from datetime import datetime
import pytz
import json
import os

app = Flask(__name__)
app.secret_key = "AQUILA_SECRET_KEY_CHANGE_ME"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "../settings.json")
USERS_FILE = os.path.join(BASE_DIR, "../users.json")

# --------------------
# Helpers
# --------------------
def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def egypt_time():
    return datetime.now(pytz.timezone("Africa/Cairo")).strftime("%H:%M:%S %d-%m-%Y")

# --------------------
# Auth
# --------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        users = load_users()
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))

        return render_template("login.html", error="بيانات الدخول غير صحيحة")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# --------------------
# Dashboard
# --------------------
@app.route("/")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    settings = load_settings()

    return render_template(
        "dashboard.html",
        time=egypt_time(),
        status=settings.get("enabled", False),
        timeframe=settings.get("timeframe", "1m"),
        pairs=settings.get("pairs", []),
        signal=settings.get("last_signal", None)
    )

# --------------------
# Start / Stop Bot
# --------------------
@app.route("/start")
def start_bot():
    settings = load_settings()
    settings["enabled"] = True
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
    return redirect(url_for("dashboard"))

@app.route("/stop")
def stop_bot():
    settings = load_settings()
    settings["enabled"] = False
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
    return redirect(url_for("dashboard"))

# --------------------
# Run
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
