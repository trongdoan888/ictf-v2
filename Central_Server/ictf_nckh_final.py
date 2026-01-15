from flask import Flask, render_template_string, request, jsonify, session
import time, threading

app = Flask(__name__)
app.secret_key = "ictf_nckh_2026_final_v2"

# --- CẤU HÌNH HỆ THỐNG ---
START_TIME = time.time()
DURATION = 3600  # 1 tiếng
# Các Flag này phải khớp với những gì bạn giấu trong DVWA
current_flags = {
    "sqli": "ICTF{SQLI_DVWA_SUCCESS_2026}",
    "xss": "ICTF{XSS_STEAL_2026}",
    "brute": "ICTF{BRUTE_FORCE_COMPLETED}"
}
leaderboard = {"Trong Doan": 0, "Team_Cyber": 850}
logs = []

# --- GIAO DIỆN DASHBOARD ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8"><title>iCTF Dashboard - Central</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; }
        .glass { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; }
        .timer { font-size: 2.5rem; font-weight: bold; color: #d29922; }
        .terminal { background: #010409; color: #7ee787; padding: 15px; border-radius: 8px; font-family: monospace; height: 180px; overflow-y: auto; border: 1px solid #30363d; }
        .badge-status { font-size: 0.7rem; padding: 5px 10px; }
    </style>
</head>
<body class="p-4">
    <div class="container-fluid">
        <div class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3">
            <div><h2 class="text-white fw-bold"><i class="fas fa-project-diagram text-primary me-2"></i> iCTF COMMAND CENTER</h2></div>
            <div class="text-center"><div class="timer" id="timer_val">60:00</div><small class="text-muted">TIME REMAINING</small></div>
            <div class="text-end text-info"><h5>TRONG DOAN</h5><span class="badge bg-danger">NCKH 2026</span></div>
        </div>

        <div class="row g-4">
            <div class="col-md-4">
                <div class="glass mb-4">
                    <h5 class="text-white mb-3"><i class="fas fa-flag-checkered me-2"></i>NỘP FLAG TỪ DVWA</h5>
                    <div class="mb-3">
                        <small class="text-muted">Target: 10.10.20.10 (TeamVM)</small>
                        <input type="text" id="flag-input" class="form-control bg-dark text-white border-secondary mb-2" placeholder="Nhập Flag lấy được...">
                        <button class="btn btn-primary w-100" onclick="submitFlag()">SUBMIT FLAG</button>
                    </div>
                </div>
                <div class="glass">
                    <h5 class="text-white mb-3"><i class="fas fa-trophy me-2"></i>BẢNG XẾP HẠNG</h5>
                    <table class="table table-dark table-hover">
                        {% for team, score in leaderboard.items() %}
                        <tr><td>{{ team }}</td><td class="text-warning fw-bold text-end">{{ score }}</td></tr>
                        {% endfor %}
                    </table>
                </div>
            </div>

            <div class="col-md-8">
                <div class="glass mb-4">
                    <div class="row text-center">
                        <div class="col-4 border-end border-secondary">
                            <small class="text-muted d-block">CENTRAL</small>
                            <span class="badge bg-success badge-status">ONLINE</span>
                        </div>
                        <div class="col-4 border-end border-secondary">
                            <small class="text-muted d-block">ROUTER</small>
                            <span class="badge bg-info badge-status">FORWARDING</span>
                        </div>
                        <div class="col-4">
                            <small class="text-muted d-block">TEAMVM (DVWA)</small>
                            <span class="badge bg-success badge-status">HTTP/80</span>
                        </div>
                    </div>
                </div>
                <div class="glass">
                    <h5 class="text-white mb-3"><i class="fas fa-terminal me-2"></i>NHẬT KÝ TẤN CÔNG (REAL-TIME)</h5>
                    <div class="terminal" id="log_box">
                        [INFO] Dashboard initialized. Watching TeamVM at 10.10.20.10...<br>
                        [INFO] Scoring engine is ready for submissions.<br>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function submitFlag() {
            const f = document.getElementById('flag-input').value;
            fetch('/api/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({flag: f})
            }).then(r => r.json()).then(d => {
                alert(d.msg);
                if(d.success) location.reload();
            });
        }
        function updateTime() {
            fetch('/api/time').then(r => r.json()).then(d => {
                document.getElementById('timer_val').innerText = d.time;
            });
        }
        setInterval(updateTime, 1000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_LAYOUT, leaderboard=leaderboard)

@app.route('/api/time')
def get_time():
    rem = int(DURATION - (time.time() - START_TIME))
    if rem <= 0: return jsonify({"time": "00:00"})
    m, s = divmod(rem, 60)
    return jsonify({"time": f"{m:02d}:{s:02d}"})

@app.route('/api/submit', methods=['POST'])
def api_submit():
    f = request.json.get('flag')
    if f in current_flags.values():
        leaderboard["Trong Doan"] += 500
        return jsonify({"success": True, "msg": "CHÍNH XÁC! Team Trong Doan được cộng 500 điểm."})
    return jsonify({"success": False, "msg": "FLAG SAI HOẶC ĐÃ HẾT HẠN!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
