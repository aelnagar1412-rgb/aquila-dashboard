from flask import Flask, render_template, redirect, url_for, session
import json
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = "aquila_secret_key"

SETTINGS_FILE = "../settings.json"
SIGNALS_FILE = "../data/signals.json"

def load_json(path, default):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default

@app.route("/")
def home():
    if not session.get("user"):
        return redirect(url_for("login"))

    settings = load_json(SETTINGS_FILE, {})
    signals = load_json(SIGNALS_FILE, [])

    cairo = pytz.timezone("Africa/Cairo")
    now = datetime.now(cairo).strftime("%H:%M:%S %d-%m-%Y")

    return render_template(
        "dashboard.html",
        status=settings.get("enabled", False),
        timeframe=settings.get("timeframe", "1m"),
        pairs=settings.get("pairs", []),
        signals=signals[-10:][::-1],
        time=now
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user"):
        return redirect(url_for("home"))

    if "POST" in str(__import__("flask").request.method):
        session["user"] = "admin"
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
