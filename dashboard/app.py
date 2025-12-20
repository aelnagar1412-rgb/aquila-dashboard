from flask import Flask, render_template, request, redirect, url_for, session
import json, os

from auth import check_login, login_required

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.json")

app = Flask(__name__)
app.secret_key = "aquila-secret-key"

def load_settings():
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]
        if check_login(user, pw):
            session["user"] = user
            return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    settings = load_settings()
    return render_template("dashboard.html", settings=settings)

@app.route("/start")
@login_required
def start_bot():
    settings = load_settings()
    settings["enabled"] = True
    save_settings(settings)
    return redirect(url_for("dashboard"))

@app.route("/stop")
@login_required
def stop_bot():
    settings = load_settings()
    settings["enabled"] = False
    save_settings(settings)
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
