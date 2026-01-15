from flask import Flask, render_template_string, request, jsonify, redirect, session
import time

app = Flask(__name__)
app.secret_key = "ictf_nckh_2026_final_pro"

# --- DỮ LIỆU HỆ THỐNG ---
game_status = "RUNNING"
scores = {"Red Team": 0, "Blue Team": 2000}
logs = [{"time": time.strftime("%H:%M:%S"), "team": "System", "msg": "Cuộc chiến bắt đầu!"}]
flags = ["ICTF{SQLI_DVWA_SUCCESS_2026}", "ICTF{XSS_STEAL_2026}"]

users = {
    "redteam": {"password": "red123", "role": "attacker", "target": "http://10.10.20.10/vulnerabilities/sqli/"},
    "blueteam": {"password": "blue123", "role": "defender", "target": "http://10.10.20.10/security.php"}
}

# --- GIAO DIỆN TỔNG QUAN (PUBLIC) ---
PUBLIC_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>Scoreboard Public</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #0b0e14; color: #adbac7; font-family: sans-serif; }
        .scoreboard { background: #1c2128; border: 1px solid #444c56; border-radius: 15px; padding: 40px; margin-top: 50px; }
        .log-container { background: #0d1117; height: 350px; overflow-y: auto; padding: 20px; border-radius: 8px; border: 1px solid #444c56; font-family: 'Courier New', monospace; }
        .point { font-size: 4rem; font-weight: bold; }
        .red-text { color: #f85149; }
        .blue-text { color: #539bf5; }
    </style>
</head>
<body>
    <div class="container scoreboard shadow-lg">
        <div class="d-flex justify-content-between align-items-center mb-5">
            <h1 class="fw-bold"><i class="fas fa-shield-virus me-3"></i>HỆ THỐNG GIÁM SÁT CHIẾN TRƯỜNG iCTF</h1>
            <a href="/login_page" class="btn btn-primary px-4">ĐĂNG NHẬP THI ĐẤU</a>
        </div>
        
        <div class="text-center mb-5">
            <h4 class="mb-4">TRẠNG THÁI: 
                {% if status == 'RUNNING' %}
                <span class="badge bg-success px-3 py-2">ĐANG DIỄN RA</span>
                {% else %}
                <span class="badge bg-danger px-3 py-2">ĐÃ KẾT THÚC</span>
                {% endif %}
            </h4>
            <div class="row">
                <div class="col-6 border-end border-secondary">
                    <h2 class="red-text">RED TEAM (ATTACK)</h2>
                    <div class="point red-text">{{ scores['Red Team'] }}</div>
                </div>
                <div class="col-6">
                    <h2 class="blue-text">BLUE TEAM (DEFENSE)</h2>
                    <div class="point blue-text">{{ scores['Blue Team'] }}</div>
                </div>
            </div>
        </div>

        <h5 class="mb-3"><i class="fas fa-stream me-2"></i>NHẬT KÝ CHIẾN TRƯỜNG</h5>
        <div class="log-container">
            {% for log in logs %}
            <div class="mb-2">
                <span class="text-muted">[{{ log.time }}]</span> 
                <b class="{% if log.team == 'Red Team' %}red-text{% elif log.team == 'Blue Team' %}blue-text{% else %}text-success{% endif %}">
                    {{ log.team }}:
                </b> 
                {{ log.msg }}
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
"""

# --- GIAO DIỆN NGƯỜI CHƠI (PRIVATE) ---
PLAYER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><title>Player Console</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #0d1117; color: #adbac7; }
        .console { border: 1px solid #444c56; background: #1c2128; border-radius: 10px; padding: 25px; }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3">
            <h3><i class="fas fa-user-circle me-2"></i>TÁC CHIẾN: <span class="text-warning">{{ user.upper() }}</span></h3>
            <a href="/logout" class="btn btn-outline-secondary btn-sm">Đăng xuất</a>
        </div>

        <div class="row g-4">
            <div class="col-md-7">
                <div class="console shadow-sm h-100">
                    <h4 class="text-white mb-4">Bảng Điều Khiển</h4>
                    <p class="h5 mb-3">Điểm của bạn: <b class="text-warning h3">{{ score }}</b></p>
                    <div class="mb-4">
                        <label class="d-block mb-2">Chiến trường (DVWA):</label>
                        <a href="{{ target }}" target="_blank" class="btn btn-primary w-100">TRUY CẬP MỤC TIÊU</a>
                    </div>
                    
                    {% if role == 'attacker' %}
                    <div class="p-3 border border-secondary rounded bg-dark">
                        <h5 class="text-success mb-3">Nộp Flag Chiếm Được</h5>
                        <div class="input-group mb-3">
                            <input type="text" id="flag" class="form-control bg-dark text-white border-secondary" placeholder="Dán Flag ICTF{...}">
                            <button class="btn btn-success" onclick="submit()">XÁC NHẬN</button>
                        </div>
                    </div>
                    <button class="btn btn-outline-danger w-100 mt-4" onclick="surrender()">ĐẦU HÀNG (DỪNG TRẬN ĐẤU)</button>
                    {% else %}
                    <div class="alert alert-info bg-dark text-info border-info">
                        Bạn đang trong vai trò Blue Team. Hãy theo dõi nhật ký tấn công và vá lỗi dịch vụ kịp thời.
                    </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="col-md-5">
                <div class="console shadow-sm" style="height: 450px; overflow-y: auto;">
                    <h5 class="text-white mb-3">Nhật ký tác chiến cá nhân</h5>
                    <div class="small font-monospace">
                        {% for log in logs %}<div class="mb-1 border-bottom border-secondary pb-1">[{{ log.time }}] {{ log.msg }}</div>{% endfor %}
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script>
        function submit() {
            const f = document.getElementById('flag').value;
            fetch('/api/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({flag: f})
            }).then(r => r.json()).then(d => { alert(d.msg); location.reload(); });
        }
        function surrender() {
            if(confirm("Xác nhận đầu hàng và kết thúc cuộc thi?")) {
                fetch('/api/surrender').then(() => { window.location.href = '/'; });
            }
        }
    </script>
</body>
</html>
"""

LOGIN_HTML = """
<body style="background:#0d1117; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif;">
    <form action="/login" method="post" style="background:#1c2128; padding:50px; border-radius:15px; border:1px solid #444c56; width:400px;">
        <h3 style="text-align:center; margin-bottom:30px;">ĐĂNG NHẬP</h3>
        <div style="margin-bottom:15px;">
            <input name="u" placeholder="Tài khoản" style="width:100%; padding:12px; background:#0b0e14; border:1px solid #444c56; color:white; border-radius:5px;">
        </div>
        <div style="margin-bottom:25px;">
            <input name="p" type="password" placeholder="Mật khẩu" style="width:100%; padding:12px; background:#0b0e14; border:1px solid #444c56; color:white; border-radius:5px;">
        </div>
        <button style="width:100%; padding:12px; background:#238636; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">VÀO CHIẾN TRƯỜNG</button>
        <div style="text-align:center; margin-top:20px;">
            <a href="/" style="color:#539bf5; text-decoration:none; font-size:0.9rem;">Quay lại Scoreboard</a>
        </div>
    </form>
</body>
"""

@app.route('/')
def public():
    return render_template_string(PUBLIC_HTML, scores=scores, logs=logs[::-1], status=game_status)

@app.route('/login_page')
def login_page():
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    u, p = request.form.get('u'), request.form.get('p')
    if u in users and users[u]['password'] == p:
        session['user'] = u
        return redirect('/dashboard')
    return "Sai thông tin đăng nhập!"

@app.route('/dashboard')
def dashboard():
    if 'user' not in session: return redirect('/login_page')
    u = session['user']
    role = users[u]['role']
    team_name = "Red Team" if role == 'attacker' else "Blue Team"
    return render_template_string(PLAYER_HTML, user=u, score=scores[team_name], 
                               target=users[u]['target'], role=role, logs=logs[::-1])

@app.route('/api/submit', methods=['POST'])
def api_submit():
    global game_status
    if game_status == "FINISHED": return jsonify({"msg": "Trận đấu đã kết thúc!"})
    f = request.json.get('flag')
    if f in flags:
        scores["Red Team"] += 500
        scores["Blue Team"] -= 500
        logs.append({"time": time.strftime("%H:%M:%S"), "team": "Red Team", "msg": "Tấn công SQLi thành công! Chiếm được 500 điểm từ Blue Team."})
        if scores["Blue Team"] <= 0:
            scores["Blue Team"] = 0
            game_status = "FINISHED"
            logs.append({"time": time.strftime("%H:%M:%S"), "team": "System", "msg": "BLUE TEAM CẠN KIỆT ĐIỂM SỐ. RED TEAM CHIẾN THẮNG TUYỆT ĐỐI!"})
        return jsonify({"msg": "FLAG CHÍNH XÁC! HỆ THỐNG GHI NHẬN ĐIỂM."})
    return jsonify({"msg": "FLAG SAI HOẶC ĐÃ HẾT HẠN!"})

@app.route('/api/surrender')
def surrender():
    global game_status
    game_status = "FINISHED"
    logs.append({"time": time.strftime("%H:%M:%S"), "team": "Red Team", "msg": "RED TEAM ĐÃ CHẤP NHẬN ĐẦU HÀNG. TRẬN ĐẤU KẾT THÚC."})
    return "OK"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
