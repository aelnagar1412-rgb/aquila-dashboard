from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/", methods=["GET", "POST"])
def dashboard():
    settings = load_settings()

    if request.method == "POST":
        settings["enabled"] = True if request.form.get("enabled") == "on" else False
        settings["timeframe"] = request.form.get("timeframe", "1m")
        pairs = request.form.get("pairs", "")
        settings["pairs"] = [p.strip().upper() for p in pairs.split(",") if p.strip()]
        save_settings(settings)
        return redirect("/")

    return render_template(
        "dashboard.html",
        enabled=settings.get("enabled", False),
        timeframe=settings.get("timeframe", "1m"),
        pairs=",".join(settings.get("pairs", []))
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
