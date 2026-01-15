from flask import Flask, render_template_string, request, redirect, jsonify
import datetime, time

app = Flask(__name__)

# Quản lý trạng thái cuộc thi
game_state = {
    "RedTeam": {"score": 0, "history": []},
    "BlueTeam": {"score": 0, "history": []},
    "start_time": time.time(),
    "vulns": {
        "sqli": {"status": "vulnerable", "last_fix_attempt": None},
        "cmd_inj": {"status": "vulnerable", "last_fix_attempt": None},
        "lfi": {"status": "vulnerable", "last_fix_attempt": None},
        "xss": {"status": "vulnerable", "last_fix_attempt": None},
        "broken_auth": {"status": "vulnerable", "last_fix_attempt": None}
    }
}

TEAM_VM_IP = "10.10.10.55"

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>iCTF Tactical Dashboard</title>
    <style>
        body { font-family: sans-serif; background: #0e1621; color: white; text-align: center; }
        .container { max-width: 1000px; margin: 30px auto; background: #17212b; padding: 20px; border-radius: 10px; }
        .score-board { display: flex; justify-content: space-around; margin: 20px 0; }
        .card { background: #242f3d; padding: 20px; border-radius: 10px; width: 45%; border-top: 5px solid; }
        .vuln-status { display: flex; justify-content: center; gap: 10px; margin: 20px 0; }
        .status-tag { padding: 5px 10px; border-radius: 4px; font-size: 0.8em; }
        .fixed { background: #2ecc71; color: white; }
        .vulnerable { background: #e74c3c; color: white; }
        .timer { font-size: 2em; color: #f1c40f; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏆 ICTF COMMAND CENTER</h1>
        <div class="timer" id="countdown">10:00</div>
        
        <div class="score-board">
            <div class="card" style="border-color: #ff4d4d;"><h2>RED TEAM: {{ red_score }}</h2></div>
            <div class="card" style="border-color: #3498db;"><h2>BLUE TEAM: {{ blue_score }}</h2></div>
        </div>

        <h3>🛠 TRẠNG THÁI HỆ THỐNG</h3>
        <div class="vuln-status">
            {% for id, info in vulns.items() %}
                <div class="status-tag {{ info.status }}">{{ id.upper() }}</div>
            {% endfor %}
        </div>

        <form action="/auth" method="POST" style="background: #242f3d; padding: 20px; border-radius: 10px;">
            <input name="team" placeholder="Team Name">
            <button style="background: #27ae60; color: white; padding: 10px;">JOIN BATTLE</button>
        </form>
    </div>
    <script>
        let timeLeft = 600; 
        setInterval(() => {
            if(timeLeft <= 0) return;
            timeLeft--;
            let m = Math.floor(timeLeft/60);
            let s = timeLeft % 60;
            document.getElementById('countdown').innerText = `${m}:${s < 10 ? '0' : ''}${s}`;
        }, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, 
                                red_score=game_state["RedTeam"]["score"], 
                                blue_score=game_state["BlueTeam"]["score"],
                                vulns=game_state["vulns"])

@app.route('/api/submit_flag', methods=['POST'])
def submit():
    data = request.json
    team = data.get('team')
    vuln_type = data.get('vuln_type', 'sqli')
    
    # Logic cộng/trừ điểm trong 10 phút
    if time.time() - game_state["start_time"] < 600:
        if game_state["vulns"][vuln_type]["status"] == "vulnerable":
            game_state["RedTeam"]["score"] += 100
            game_state["BlueTeam"]["score"] -= 50
            return jsonify({"status": "captured"})
    return jsonify({"status": "round_ended_or_fixed"})

@app.route('/api/commit_fix', methods=['POST'])
def commit_fix():
    vuln_type = request.json.get('vuln_type')
    if vuln_type in game_state["vulns"]:
        game_state["vulns"][vuln_type]["status"] = "fixed"
        game_state["BlueTeam"]["score"] += 200
        return jsonify({"status": "success"})
    return jsonify({"status": "error"})

@app.route('/auth', methods=['POST'])
def auth():
    t = request.form.get('team')
    return redirect(f"http://{TEAM_VM_IP}/{'red' if 'Red' in t else 'blue'}-portal")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
