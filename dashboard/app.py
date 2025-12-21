from flask import Flask, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

@app.route("/")
def index():
    egypt_time = datetime.now(pytz.timezone("Africa/Cairo")).strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "status": "ON",
        "timeframe": "1m",
        "pairs": ["EURUSD", "EURJPY", "EURGBP", "AUDCAD", "USDJPY"],
        "time": egypt_time,
        "signals": []
    }

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
