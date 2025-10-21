from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Team1 Service Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9001)
