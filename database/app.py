from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import Base, Flag, Score

DB_FILE = os.environ.get("DB_FILE", "sqlite:///data/ictf.db")
engine = create_engine(DB_FILE, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

app = Flask(__name__)

@app.route("/set_flag", methods=["POST"])
def set_flag():
    data = request.json or {}
    team = data.get("team")
    flag = data.get("flag")
    if not team or not flag:
        return jsonify({"error": "invalid payload"}), 400
    s = Session()
    f = Flag(team=team, flag=flag)
    s.add(f)
    s.commit()
    s.close()
    return jsonify({"status": "ok"}), 200

@app.route("/get_flag/<team>", methods=["GET"])
def get_flag(team):
    s = Session()
    f = s.query(Flag).filter_by(team=team).order_by(Flag.id.desc()).first()
    s.close()
    if not f:
        return jsonify({"flag": "no_flag"}), 200
    return jsonify({"flag": f.flag}), 200

@app.route("/submit_flag", methods=["POST"])
def submit_flag():
    data = request.json or {}
    submitting_team = data.get("team")
    flag = data.get("flag")
    if not submitting_team or not flag:
        return jsonify({"error": "invalid payload"}), 400
    s = Session()
    f = s.query(Flag).filter_by(flag=flag).first()
    if f:
        score_row = s.query(Score).filter_by(team=submitting_team).first()
        if not score_row:
            score_row = Score(team=submitting_team, score=0)
            s.add(score_row)
        score_row.score += 10
        s.commit()
        ret = {"result": "correct", "score": score_row.score}
    else:
        ret = {"result": "wrong"}
    s.close()
    return jsonify(ret), 200

@app.route("/scores", methods=["GET"])
def scores():
    s = Session()
    rows = s.query(Score).all()
    s.close()
    data = {r.team: r.score for r in rows}
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
