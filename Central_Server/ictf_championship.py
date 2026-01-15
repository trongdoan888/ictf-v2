from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import time, random, string, threading

app = Flask(__name__)
app.secret_key = "ictf_championship_key_2026"

START_TIME = time.time()
DURATION = 3600
current_flags = {}
CHALLENGE_KEYS = ["sqli", "rce", "idor", "logic", "traversal"]

def generate_flag():
    return "ICTF{" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12)) + "}"

def update_flags_periodically():
    while True:
        for key in CHALLENGE_KEYS:
            current_flags[key] = generate_flag()
        time.sleep(300)

threading.Thread(target=update_flags_periodically, daemon=True).start()

CHALLENGES = {
    "sqli": {"name": "SQL Injection", "vuln": "login.php", "path": "/var/www/html/auth.php"},
    "rce": {"name": "Command Injection", "vuln": "ping.php", "path": "/var/www/html/net.php"},
    "idor": {"name": "IDOR", "vuln": "user_profile", "path": "/api/v1/users.py"},
    "logic": {"name": "Logic Auth", "vuln": "cookie_check", "path": "/js/session.js"},
    "traversal": {"name": "Path Traversal", "vuln": "file_view", "path": "/opt/apps/files.py"}
}

# --- HTML TEMPLATES (Sửa lỗi Syntax) ---
DASHBOARD_HTML = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    body { background: #0f172a; color: #f1f5f9; font-family: 'Inter', sans-serif; }
    .glass { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; padding: 20px; }
    .timer { font-size: 1.5rem; font-weight: bold; color: #fbbf24; }
</style>
<div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-5 glass">
        <div><h4>User: <span class="text-primary">{{ user }}</span> | Team: <span class="text-uppercase {{ 'text-danger' if team=='red' else 'text-info' }}">{{ team }}</span></h4></div>
        <div class="timer">KẾT THÚC TRONG: {{ timer_str }}</div>
    </div>
    <div class="row g-4">
        {% if team == 'red' %}
            <h3 class="text-danger"><i class="fas fa-bullseye"></i> MỤC TIÊU KHAI THÁC</h3>
            {% for id, info in challenges.items() %}
            <div class="col-md-4">
                <div class="glass h-100 text-center border-bottom border-danger border-3">
                    <h5>{{ info.name }}</h5>
                    <p class="small text-muted">Lỗ hổng: {{ info.vuln }}</p>
                    <a href="/exploit/{{id}}" class="btn btn-outline-danger w-100">ATTACK</a>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <h3 class="text-info"><i class="fas fa-shield-virus"></i> HỆ THỐNG CẦN BẢO MỆT</h3>
            {% for id, info in challenges.items() %}
            <div class="col-md-6">
                <div class="glass mb-3 border-start border-info border-4">
                    <h5 class="text-info">{{ info.name }}</h5>
                    <p class="mb-1">Vị trí file: <code>{{ info.path }}</code></p>
                    <p class="small text-warning"><i class="fas fa-code-branch"></i> Trạng thái: Cần vá lỗi</p>
                    <a href="/fix/{{id}}" class="btn btn-sm btn-info text-white">XEM CHI TIẾT</a>
                </div>
            </div>
            {% endfor %}
        {% endif %}
    </div>
</div>
<script>setTimeout(() => location.reload(), 5000);</script>
"""

@app.route('/')
def entry():
    return render_template_string("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body { background: #0f172a; color: white; }</style>
    <div class="container vh-100 d-flex justify-content-center align-items-center">
        <div class="p-5 bg-dark border border-secondary rounded shadow-lg text-center">
            <h2 class="mb-4 text-primary">iCTF CHAMPIONSHIP 2026</h2>
            <form action="/join" method="POST">
                <input type="text" name="username" class="form-control mb-3 bg-dark text-white border-secondary" placeholder="Tên đấu thủ" required>
                <div class="d-flex gap-3">
                    <button name="team" value="red" class="btn btn-danger w-100">RED TEAM</button>
                    <button name="team" value="blue" class="btn btn-primary w-100">BLUE TEAM</button>
                </div>
            </form>
        </div>
    </div>
    """)

@app.route('/join', methods=['POST'])
def join():
    session['user'] = request.form.get('username')
    session['team'] = request.form.get('team')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/')
    remaining = int(DURATION - (time.time() - START_TIME))
    if remaining <= 0: return "<h1 style='color:white;text-align:center;'>CUỘC THI KẾT THÚC</h1>"
    mins, secs = divmod(remaining, 60)
    return render_template_string(DASHBOARD_HTML, user=session['user'], team=session['team'], 
                                 challenges=CHALLENGES, timer_str=f"{mins:02d}:{secs:02d}")

@app.route('/exploit/<id>')
def exploit_page(id):
    return render_template_string("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <body style="background:#0f172a; color:white; padding:50px;">
        <div class="container text-center">
            <h1>Khai thác {{name}}</h1>
            <div class="p-4 bg-dark border border-danger rounded mt-4">
                <input type="text" id="p" class="form-control mb-3 bg-dark text-white" placeholder="Nhập Payload">
                <button onclick="run()" class="btn btn-danger w-100">RUN EXPLOIT</button>
                <div id="res" class="mt-4 p-3 bg-black text-success rounded d-none"></div>
            </div>
            <a href="/dashboard" class="btn btn-link mt-3 text-muted">Quay lại Dashboard</a>
        </div>
        <script>
            function run() {
                fetch('/api/attack/{{id}}', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({p: document.getElementById('p').value})
                }).then(r => r.json()).then(d => {
                    document.getElementById('res').classList.remove('d-none');
                    document.getElementById('res').innerText = d.msg;
                });
            }
        </script>
    </body>
    """, id=id, name=CHALLENGES[id]['name'])

@app.route('/api/attack/<id>', methods=['POST'])
def api_attack(id):
    p = request.json.get('p', '')
    if (id == 'sqli' and "' OR 1=1" in p) or (id == 'rce' and ";" in p):
        return jsonify({"msg": f"SUCCESS! Flag: {current_flags.get(id, 'FLAG_GENERATING')}"})
    return jsonify({"msg": "Exploit failed!"})

@app.route('/fix/<id>')
def fix_page(id):
    return f"<body style='background:#0f172a;color:white;padding:50px;'><h2>Mã nguồn: {CHALLENGES[id]['path']}</h2><p>Vui lòng vá lỗi trực tiếp trên máy ảo.</p><a href='/dashboard'>Quay lại</a></body>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
