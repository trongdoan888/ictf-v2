from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ictf_secret_key' # Cần thiết để sử dụng session (lưu tên đội)

# Giao diện Glassmorphism hiện đại
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>iCTF - Trung Tâm Điều Hành</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root { --primary: #3b82f6; --red: #ef4444; --blue: #10b981; --bg: #0b0f1a; --card: rgba(30, 41, 59, 0.7); }
        body { background: var(--bg); color: #f1f5f9; font-family: 'Segoe UI', sans-serif; min-height: 100vh; }
        .glass { background: var(--card); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; }
        .terminal { background: #000; color: #38bdf8; padding: 15px; font-family: 'Consolas', monospace; border-radius: 10px; font-size: 0.85rem; border: 1px solid #334155; height: 200px; overflow-y: auto; }
        .navbar { background: rgba(15, 23, 42, 0.9); border-bottom: 1px solid rgba(59, 130, 246, 0.3); }
        .btn-action { border-radius: 10px; font-weight: bold; text-transform: uppercase; }
        .status-up { color: var(--blue); font-weight: bold; }
        .challenge-box { border-left: 4px solid var(--primary); background: rgba(255,255,255,0.05); transition: 0.3s; }
        .challenge-box:hover { background: rgba(255,255,255,0.1); }
    </style>
</head>
<body>
    {{ content | safe }}
</body>
</html>
"""

# --- ROUTE 1: TRANG ĐĂNG NHẬP TÊN ĐỘI ---
@app.route('/')
def login():
    content = """
    <div class="container d-flex align-items-center justify-content-center" style="height: 100vh;">
        <div class="glass p-5 text-center" style="width: 450px;">
            <i class="fas fa-user-circle fa-4x text-primary mb-4"></i>
            <h2 class="fw-bold mb-4">ĐĂNG NHẬP HỆ THỐNG</h2>
            <form action="/set_team" method="POST">
                <div class="mb-4">
                    <input type="text" name="team_name" class="form-control form-control-lg bg-dark text-white border-secondary text-center" placeholder="Nhập tên đội của bạn" required>
                </div>
                <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold">TIẾP TỤC</button>
            </form>
            <p class="mt-4 text-muted small">Môi trường diễn tập An toàn thông tin iCTF</p>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

@app.route('/set_team', methods=['POST'])
def set_team():
    session['team_name'] = request.form.get('team_name')
    return redirect(url_for('portal'))

# --- ROUTE 2: SẢNH CHÍNH (CHỌN VAI TRÒ) ---
@app.route('/portal')
def portal():
    team_name = session.get('team_name', 'Khách')
    content = f"""
    <div class="container d-flex flex-column align-items-center justify-content-center" style="height: 100vh;">
        <h1 class="fw-bold mb-2"><i class="fas fa-microchip text-primary"></i> iCTF COMMAND PORTAL</h1>
        <h4 class="text-info mb-5">Chào mừng đội: <span class="text-warning">{team_name}</span></h4>
        <div class="d-flex gap-4">
            <div class="glass p-4 text-center role-card" style="width: 300px;">
                <i class="fas fa-user-secret fa-4x text-danger mb-4"></i>
                <h3 class="fw-bold">RED TEAM</h3>
                <a href="/battleground/red" class="btn btn-danger w-100 py-2 fw-bold">VÀO TẤN CÔNG</a>
            </div>
            <div class="glass p-4 text-center role-card" style="width: 300px;">
                <i class="fas fa-user-shield fa-4x text-success mb-4"></i>
                <h3 class="fw-bold">BLUE TEAM</h3>
                <a href="/battleground/blue" class="btn btn-success w-100 py-2 fw-bold">VÀO PHÒNG THỦ</a>
            </div>
            <div class="glass p-4 text-center role-card" style="width: 300px;">
                <i class="fas fa-trophy fa-4x text-warning mb-4"></i>
                <h3 class="fw-bold">SCOREBOARD</h3>
                <a href="/scoreboard" class="btn btn-warning w-100 py-2 fw-bold text-dark">BẢNG ĐIỂM</a>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

# --- ROUTE 3: CHIẾN TRƯỜNG RED TEAM (CHI TIẾT BÀI TẤN CÔNG) ---
@app.route('/battleground/red')
def red_battleground():
    team_name = session.get('team_name', 'Khách')
    challenges = [
        {"id": "SQLi", "name": "SQL Injection", "target": "10.10.20.20/login.php", "desc": "Khai thác lỗi đăng nhập để lấy thông tin người dùng."},
        {"id": "CMD", "name": "Command Injection", "target": "10.10.20.20/ping.php", "desc": "Thực thi lệnh hệ thống từ xa (RCE) để đọc file /flag.txt."},
        {"id": "UPLOAD", "name": "Unrestricted File Upload", "target": "10.10.20.20/upload.php", "desc": "Tải lên Web Shell để chiếm quyền điều khiển máy chủ."},
        {"id": "AUTH", "name": "Broken Authentication", "target": "10.10.20.20/admin", "desc": "Bypass cơ chế xác thực để truy cập trang quản trị."},
        {"id": "PRIVESC", "name": "Privilege Escalation", "target": "10.10.20.20 (SSH)", "desc": "Leo thang đặc quyền từ user thường lên root via SUID."}
    ]
    
    challenge_html = "".join([f"""
    <div class="glass p-3 mb-3 challenge-box">
        <div class="d-flex justify-content-between align-items-center">
            <div>
                <h6 class="text-danger fw-bold mb-1">[{c['id']}] {c['name']}</h6>
                <small class="text-info">Mục tiêu: {c['target']}</small><br>
                <small class="text-muted">{c['desc']}</small>
            </div>
            <button class="btn btn-sm btn-outline-danger">Khai thác</button>
        </div>
    </div>
    """ for c in challenges])

    content = f"""
    <nav class="navbar navbar-dark py-3 px-4 shadow mb-4">
        <span class="navbar-brand fw-bold text-danger"><i class="fas fa-skull"></i> RED TEAM: {team_name}</span>
        <a href="/portal" class="btn btn-outline-light btn-sm">QUAY LẠI</a>
    </nav>
    <div class="container">
        <div class="row">
            <div class="col-md-7">
                <h5 class="mb-3">DANH SÁCH BÀI TẤN CÔNG</h5>
                {challenge_html}
            </div>
            <div class="col-md-5">
                <div class="glass p-4 mb-4">
                    <h5 class="text-warning fw-bold mb-3"><i class="fas fa-flag"></i> NỘP FLAG</h5>
                    <input type="text" class="form-control bg-dark text-white border-secondary mb-2" placeholder="iCTF{{...}}">
                    <button class="btn btn-danger w-100">XÁC NHẬN FLAG</button>
                </div>
                <div class="glass p-4 h-50">
                    <h5 class="text-info fw-bold mb-3"><i class="fas fa-terminal"></i> LOGS TẤN CÔNG</h5>
                    <div class="terminal">
                        [READY] Đội {team_name} đã sẵn sàng...<br>
                        [SCAN] Đang quét lỗ hổng bài SQLi...<br>
                        <span class="text-white">_</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

# --- ROUTE 4: CHIẾN TRƯỜNG BLUE TEAM (CHI TIẾT PHÒNG THỦ) ---
@app.route('/battleground/blue')
def blue_battleground():
    team_name = session.get('team_name', 'Khách')
    content = f"""
    <nav class="navbar navbar-dark py-3 px-4 shadow mb-4">
        <span class="navbar-brand fw-bold text-success"><i class="fas fa-user-shield"></i> BLUE TEAM: {team_name}</span>
        <a href="/portal" class="btn btn-outline-light btn-sm">QUAY LẠI</a>
    </nav>
    <div class="container">
        <div class="row text-center mb-4">
            <div class="col-md-4"><div class="glass p-3"><h6>Dịch Vụ</h6><h2 class="status-up">ONLINE</h2></div></div>
            <div class="col-md-4"><div class="glass p-3"><h6>Bài đã vá</h6><h2 class="text-primary">3/5</h2></div></div>
            <div class="col-md-4"><div class="glass p-3"><h6>SLA Score</h6><h2 class="text-warning">98%</h2></div></div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="glass p-4">
                    <h5 class="text-success fw-bold mb-3">HƯỚNG DẪN VÁ LỖ HỔNG (DEFENSE GUIDE)</h5>
                    <div class="list-group list-group-flush bg-transparent">
                        <div class="list-group-item bg-transparent text-white border-secondary">1. SQLi: Kiểm tra file <code>/var/www/html/login.php</code>, dùng <code>mysqli_real_escape_string</code>.</div>
                        <div class="list-group-item bg-transparent text-white border-secondary">2. RCE: Kiểm tra file <code>ping.php</code>, chặn ký tự <code>; | &</code>.</div>
                        <div class="list-group-item bg-transparent text-white border-secondary">3. Upload: Giới hạn file tại <code>/etc/apache2/conf-available</code>.</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

# --- ROUTE 5: SCOREBOARD ---
@app.route('/scoreboard')
def scoreboard():
    teams = [{"rank": 1, "name": "Team Alpha", "pts": 2500}, {"rank": 2, "name": "Team Bravo", "pts": 1800}]
    rows = "".join([f"<tr><td>{t['rank']}</td><td>{t['name']}</td><td>{t['pts']}</td></tr>" for t in teams])
    content = f"""
    <nav class="navbar navbar-dark py-3 px-4 shadow mb-4">
        <span class="navbar-brand fw-bold text-warning">SCOREBOARD</span>
        <a href="/portal" class="btn btn-outline-light btn-sm text-dark">QUAY LẠI</a>
    </nav>
    <div class="container glass p-0 overflow-hidden text-center">
        <table class="table table-dark table-hover mb-0">
            <thead class="table-primary text-dark"><tr><th>Hạng</th><th>Tên Đội</th><th>Điểm</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """
    return render_template_string(BASE_TEMPLATE, content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
