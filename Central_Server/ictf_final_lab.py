from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import time, random, string, threading

app = Flask(__name__)
app.secret_key = "ictf_master_key_2026"

# --- BIẾN HỆ THỐNG ---
START_TIME = time.time()
DURATION = 3600  # 1 giờ
current_flags = {}
CHALLENGE_KEYS = ["sqli", "rce", "idor", "logic", "traversal"]

def generate_flag():
    return "ICTF{" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12)) + "}"

def update_flags():
    while True:
        for key in CHALLENGE_KEYS:
            current_flags[key] = generate_flag()
        time.sleep(300) # 5 phút

threading.Thread(target=update_flags, daemon=True).start()

CHALLENGES = {
    "sqli": {"name": "SQL Injection Portal", "vuln": "login.php", "port": "8081", "desc": "Bypass Admin Login"},
    "rce": {"name": "Network Diagnostics", "vuln": "ping.php", "port": "8082", "desc": "Command Injection RCE"},
    "idor": {"name": "User Management", "vuln": "user.php", "port": "8083", "desc": "Insecure Object Reference"},
    "logic": {"name": "Admin Control", "vuln": "auth.js", "port": "8084", "desc": "Privilege Escalation"},
    "traversal": {"name": "Cloud Storage", "vuln": "files.py", "port": "8085", "desc": "Path Traversal"}
}

# --- GIAO DIỆN TỔNG HỢP ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>iCTF Ultimate Lab - {{ session.get('user', 'Guest') }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #0b0f1a; color: #f1f5f9; font-family: 'Segoe UI', sans-serif; }
        .glass { background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; transition: 0.3s; }
        .card-red { border-left: 5px solid #ef4444; }
        .card-blue { border-left: 5px solid #3b82f6; }
        .timer { font-size: 2rem; font-weight: bold; color: #fbbf24; text-shadow: 0 0 10px rgba(251, 191, 36, 0.5); }
        .terminal { background: #000; color: #4ade80; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.9rem; border: 1px solid #334155; }
        .btn-cyber { background: transparent; border: 1px solid #3b82f6; color: #3b82f6; font-weight: bold; }
        .btn-cyber:hover { background: #3b82f6; color: white; box-shadow: 0 0 15px #3b82f6; }
    </style>
</head>
<body>

{% if not session.get('user') %}
    <div class="container vh-100 d-flex justify-content-center align-items-center">
        <div class="glass p-5 text-center shadow-lg" style="width: 450px;">
            <h1 class="text-primary fw-bold mb-2">iCTF 2026</h1>
            <p class="text-muted mb-4 text-uppercase">Attack-Defense Simulation</p>
            <form action="/join" method="POST">
                <input type="text" name="username" class="form-control mb-3 bg-dark text-white border-secondary" placeholder="Tên Đấu Thủ" required>
                <div class="d-flex gap-2">
                    <button name="team" value="red" class="btn btn-outline-danger w-50 fw-bold">RED TEAM</button>
                    <button name="team" value="blue" class="btn btn-outline-info w-50 fw-bold">BLUE TEAM</button>
                </div>
            </form>
        </div>
    </div>
{% else %}
    <nav class="navbar border-bottom border-secondary p-3 mb-4">
        <div class="container d-flex justify-content-between align-items-center">
            <span class="fw-bold text-primary"><i class="fas fa-microchip me-2"></i> TRONG DOAN | {{ session.team|upper }}</span>
            <div class="timer" id="timer">--:--</div>
            <a href="/logout" class="btn btn-sm btn-outline-secondary">Thoát</a>
        </div>
    </nav>

    <div class="container">
        <div class="row g-4">
            <div class="col-md-7">
                <h4 class="text-danger mb-4"><i class="fas fa-skull-crossbones me-2"></i> ATTACK INTERFACE</h4>
                {% for id, info in challenges.items() %}
                <div class="glass card-red p-3 mb-3">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h5 class="fw-bold mb-1">{{ info.name }}</h5>
                            <small class="text-muted">Target: 10.10.10.10:{{ info.port }} | Vuln: {{ info.vuln }}</small>
                        </div>
                        <button class="btn btn-sm btn-cyber" onclick="showExploit('{{id}}')">OPEN EXPLOIT</button>
                    </div>
                    <div id="box-{{id}}" class="mt-3 d-none">
                        <div class="input-group">
                            <input type="text" id="payload-{{id}}" class="form-control bg-dark text-white border-secondary" placeholder="Payload...">
                            <button class="btn btn-danger" onclick="execute('{{id}}')">ATTACK</button>
                        </div>
                        <div id="res-{{id}}" class="terminal mt-2"></div>
                    </div>
                </div>
                {% endfor %}
            </div>

            <div class="col-md-5">
                <h4 class="text-info mb-4"><i class="fas fa-shield-halved me-2"></i> DEFENSE MONITOR</h4>
                <div class="glass p-3 mb-4">
                    <h6 class="text-warning fw-bold mb-3"><i class="fas fa-triangle-exclamation"></i> LỖ HỔNG PHÁT HIỆN</h6>
                    {% for id, info in challenges.items() %}
                    <div class="border-start border-warning p-2 mb-2 bg-dark rounded small">
                        <b>{{ info.name }}:</b> Cần vá file <code>{{ info.vuln }}</code>
                        <br><span class="text-muted">SLA: 100% | Status: Online</span>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="glass p-3">
                    <h6 class="text-primary fw-bold mb-3"><i class="fas fa-flag"></i> NỘP FLAG CHIẾN TRƯỜNG</h6>
                    <input type="text" id="flag-input" class="form-control mb-2 bg-dark text-white" placeholder="Dán Flag lấy được vào đây...">
                    <button class="btn btn-primary w-100 fw-bold" onclick="submitFlag()">SUBMIT FLAG</button>
                </div>
            </div>
        </div>
    </div>
{% endif %}

<script>
    function showExploit(id) { document.getElementById('box-' + id).classList.toggle('d-none'); }

    function execute(id) {
        const p = document.getElementById('payload-' + id).value;
        fetch('/api/attack', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({id: id, payload: p})
        }).then(r => r.json()).then(data => {
            document.getElementById('res-' + id).innerText = data.result;
        });
    }

    function submitFlag() {
        const flag = document.getElementById('flag-input').value;
        fetch('/api/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({flag: flag})
        }).then(r => r.json()).then(data => alert(data.msg));
    }

    // Timer logic
    setInterval(() => {
        fetch('/api/time').then(r => r.json()).then(data => {
            document.getElementById('timer').innerText = data.time;
            if(data.end) location.reload();
        });
    }, 1000);
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, challenges=CHALLENGES)

@app.route('/join', methods=['POST'])
def join():
    session['user'] = request.form.get('username')
    session['team'] = request.form.get('team')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/api/time')
def get_time():
    rem = int(DURATION - (time.time() - START_TIME))
    if rem <= 0: return jsonify({"time": "END", "end": True})
    m, s = divmod(rem, 60)
    return jsonify({"time": f"{m:02d}:{s:02d}", "end": False})

@app.route('/api/attack', methods=['POST'])
def api_attack():
    data = request.json
    id, p = data.get('id'), data.get('payload', '')
    res = "Exploit Failed."
    if (id == 'sqli' and "' OR 1=1" in p) or (id == 'rce' and ";" in p) or (id == 'traversal' and "../" in p):
        res = f"SUCCESS! Captured Flag: {current_flags.get(id)}"
    return jsonify({"result": res})

@app.route('/api/submit', methods=['POST'])
def api_submit():
    flag = request.json.get('flag')
    if flag in current_flags.values():
        return jsonify({"msg": "FLAG CHÍNH XÁC! Hệ thống đã ghi nhận điểm cho đội của bạn."})
    return jsonify({"msg": "Sai Flag hoặc Flag đã hết hạn."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
