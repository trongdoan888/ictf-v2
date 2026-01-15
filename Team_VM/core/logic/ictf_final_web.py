from flask import Flask, render_template_string, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = 'nckh_secret'

def get_logs():
    if os.path.exists('/opt/ictf/gamebot/nckh_results.log'):
        with open('/opt/ictf/gamebot/nckh_results.log', 'r') as f:
            return f.readlines()[-10:]
    return []

@app.route('/')
def scoreboard():
    logs = get_logs()
    return render_template_string('''
        <body style="background:#0d1117; color:#c9d1d9; font-family:sans-serif; text-align:center;">
            <h1 style="color:#58a6ff;">📊 iCTF ATTACK-DEFENSE SCOREBOARD</h1>
            <div style="display:flex; justify-content:center; gap:20px; margin-top:20px;">
                <div style="background:#161b22; padding:20px; border-radius:10px; border:1px solid #30363d; width:40%;">
                    <h2 style="color:#3fb950;">Bảng Xếp Hạng</h2>
                    <table border="1" style="width:100%; border-collapse:collapse;">
                        <tr style="background:#21262d;"><th>Rank</th><th>Team</th><th>Score</th><th>Status</th></tr>
                        <tr><td>1</td><td>Team_Test (ID:1)</td><td>{{ logs|length * 10 }}</td><td style="color:#3fb950;">ONLINE</td></tr>
                    </table>
                </div>
                <div style="background:#161b22; padding:20px; border-radius:10px; border:1px solid #30363d; width:40%;">
                    <h2 style="color:#f85149;">Sự Kiện Hệ Thống</h2>
                    <ul style="text-align:left; font-size:12px;">
                        {% for log in logs %} <li>{{ log }}</li> {% endfor %}
                    </ul>
                </div>
            </div>
            <p style="margin-top:30px;"><a href="/login" style="color:#8b949e; text-decoration:none;">[ Quản lý Đội chơi ]</a></p>
        </body>
    ''', logs=logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        u = request.form.get('u')
        if u == 'red': return redirect('/red_dashboard')
        if u == 'blue': return redirect('/blue_dashboard')
    return '<body style="background:#0d1117; color:white; text-align:center; padding-top:100px;"><h2>Login</h2><form method="POST"><input name="u" placeholder="User (red/blue)"><button>Enter</button></form></body>'

@app.route('/red_dashboard')
def red():
    return '<body style="background:#0d1117; color:#f85149; padding:40px;"><h1>⚔️ RED TEAM CONSOLE</h1><hr><p><b>Mục tiêu:</b> 172.18.0.x (web_service)</p><p><b>Vulnerabilities:</b> SQL Injection, LFI</p><a href="/">Quay lại</a></body>'

@app.route('/blue_dashboard')
def blue():
    return '<body style="background:#0d1117; color:#3fb950; padding:40px;"><h1>🛡️ BLUE TEAM CONSOLE</h1><hr><p><b>Dịch vụ bảo vệ:</b> web_service (Port 80)</p><p><b>Trạng thái:</b> Sẵn sàng</p><a href="/">Quay lại</a></body>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
