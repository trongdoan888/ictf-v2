from flask import Flask, render_template
import requests, os

app = Flask(__name__, template_folder="templates")
DB_URL = os.environ.get("DB_URL", "http://database:5000")

@app.route("/")
def index():
    try:
        r = requests.get(f"{DB_URL}/scores", timeout=3)
        scores = r.json()
    except Exception:
        scores = {"error": "cannot fetch scores"}
    return render_template("index.html", scores=scores)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
