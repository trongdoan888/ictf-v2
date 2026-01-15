from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)
app.secret_key = "ictf_ultimate_2026"

CHALLENGES = {
    "sqli": {"name": "SQL Injection Portal", "flag": "ICTF{SQLi_Master_2026}", "vuln": "Lỗ hổng tại login.php - Nối chuỗi SQL"},
    "rce": {"name": "Network Diagnostics", "flag": "ICTF{RCE_System_Pwned_2026}", "vuln": "Lỗ hổng tại ping.php - Thiếu lọc ký tự đặc biệt"},
    "idor": {"name": "User Management", "flag": "ICTF{IDOR_Admin_Access_2026}", "vuln": "Lỗ hổng tại user.php - Không kiểm tra quyền ID"},
    "logic": {"name": "Admin Control Panel", "flag": "ICTF{Cookie_Manipulator_2026}", "vuln": "Lỗ hổng tại auth.js - Tin tưởng Cookie phía Client"},
    "traversal": {"name": "Cloud Storage Explorer", "flag": "ICTF{Path_Leak_2026}", "vuln": "Lỗ hổng tại files.php - Directory Traversal"}
}

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8"><title>iCTF Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body { background: #0f172a; color: #f1f5f9; }
        .glass { background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); border-radius: 15px; }
        .challenge-box { transition: 0.3s; cursor: pointer; border-left: 4px solid #ef4444; }
        .challenge-box:hover { background: #334155; transform: translateY(-5px); }
        .defense-alert { border-left: 4px solid #10b981; background: rgba(16, 185, 129, 0.1); }
    </style>
</head>
<body class="p-4">
    <div class="container">
        <h2 class="text-center fw-bold text-primary mb-5"><i class="fas fa-shield-halved"></i> iCTF ATTACK-DEFENSE PLATFORM</h2>
        <div class="row g-4">
            <div class="col-md-7">
                <h4 class="text-danger mb-4"><i class="fas fa-gun"></i> CHIẾN TRƯỜNG (RED TEAM)</h4>
                {% for id, info in challenges.items() %}
                <div class="glass challenge-box p-3 mb-3" onclick="location.href='/challenge/{{id}}'">
                    <div class="d-flex justify-content-between">
                        <h5 class="fw-bold">{{ info.name }}</h5>
                        <i class="fas fa-external-link-alt text-muted"></i>
                    </div>
                    <p class="small text-muted mb-0">Nhấn để truy cập môi trường khai thác...</p>
                </div>
                {% endfor %}
            </div>
            <div class="col-md-5">
                <h4 class="text-success mb-4"><i class="fas fa-user-shield"></i> GIÁM SÁT (BLUE TEAM)</h4>
                <div class="glass p-4">
                    <h6 class="fw-bold mb-3">CẢNH BÁO LỖ HỔNG HỆ THỐNG</h6>
                    {% for id, info in challenges.items() %}
                    <div class="defense-alert p-2 mb-2 rounded small">
                        <i class="fas fa-exclamation-triangle text-warning me-2"></i> {{ info.vuln }}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

CHALLENGE_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8"><title>{{name}}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background: #1e293b; color: white; padding-top: 50px; }
        .terminal { background: #000; color: #4ade80; padding: 20px; border-radius: 10px; font-family: monospace; height: 150px; overflow-y: auto; }
        .input-dark { background: #0f172a; border: 1px solid #334155; color: white; }
    </style>
</head>
<body>
    <div class="container text-center">
        <a href="/" class="btn btn-sm btn-outline-secondary mb-4">← Quay lại Dashboard</a>
        <h1 class="mb-4">{{name}}</h1>
        <div class="row justify-content-center">
            <div class="col-md-6 card bg-dark p-4 shadow">
                <input type="text" id="payload" class="form-control input-dark mb-3" placeholder="Nhập Payload khai thác...">
                <button onclick="attack()" class="btn btn-danger w-100">THỰC THI KHAI THÁC</button>
            </div>
        </div>
        <div class="row justify-content-center mt-4 d-none" id="result-box">
            <div class="col-md-8">
                <div class="terminal" id="output"></div>
            </div>
        </div>
    </div>
    <script>
        function attack() {
            const p = document.getElementById('payload').value;
            fetch('/exploit/{{type}}', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({payload: p})
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('result-box').classList.remove('d-none');
                document.getElementById('output').innerText = data.result;
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DASHBOARD_HTML, challenges=CHALLENGES)

@app.route('/challenge/<id>')
def challenge(id):
    if id in CHALLENGES:
        return render_template_string(CHALLENGE_HTML, name=CHALLENGES[id]['name'], type=id)
    return "Not Found", 404

@app.route('/exploit/<id>', methods=['POST'])
def exploit(id):
    p = request.json.get('payload', '')
    res = "Tấn công thất bại. Thử lại với payload khác."
    if id == 'sqli' and "' OR 1=1" in p:
        res = f"Bypass thành công! Welcome Admin. FLAG: {CHALLENGES[id]['flag']}"
    elif id == 'rce' and ";" in p:
        res = f"Ping output... [VULNERABLE] root:x:0:0:root\\nFLAG: {CHALLENGES[id]['flag']}"
    elif id == 'idor' and p == "1":
        res = f"Dữ liệu Admin: {CHALLENGES[id]['flag']}"
    elif id == 'logic' and "admin=true" in p.lower():
        res = f"Quyền Admin được xác nhận! FLAG: {CHALLENGES[id]['flag']}"
    elif id == 'traversal' and "../" in p:
        res = f"Đọc file /etc/passwd thành công! FLAG: {CHALLENGES[id]['flag']}"
    return jsonify({"result": res})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
