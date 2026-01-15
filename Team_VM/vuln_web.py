from flask import Flask, request, render_template_string, send_file, jsonify
import os, sqlite3, requests

app = Flask(__name__)
SERVER_API = "http://10.10.10.45:5000/api"
@app.route('/')
def index():
    return """
    <div style="text-align:center; margin-top:50px; font-family:sans-serif;">
        <h1>WELCOME TO iCTF BATTLEGROUND</h1>
        <a href="/red-portal"><button style="background:red; color:white; padding:20px;">VÀO RED TEAM (Tấn công)</button></a>
        <a href="/blue-portal"><button style="background:blue; color:white; padding:20px;">VÀO BLUE TEAM (Phòng thủ)</button></a>
    </div>
    """

# --- UI TEMPLATE ---
def get_nav(team_color):
    return f"""<div style="background:{team_color};padding:15px;color:white;text-align:center;font-weight:bold;">
    iCTF BATTLEGROUND - TEAM VM</div>"""

@app.route('/red-portal')
def red():
    return render_template_string(get_nav("#c0392b") + """
    <div style="padding:20px; font-family:sans-serif;">
        <h1>🚩 RED TEAM MISSION</h1>
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px;">
            <a href="/sqli"><button>1. SQLi</button></a>
            <a href="/cmd"><button>2. CMD Inj</button></a>
            <a href="/lfi"><button>3. LFI</button></a>
            <a href="/xss"><button>4. XSS</button></a>
            <a href="/auth-bypass"><button>5. Broken Auth</button></a>
        </div>
    </div>
    <style>button{width:100%; padding:20px; cursor:pointer; background:#f8d7da; border:1px solid #c0392b;}</style>
    """)

@app.route('/blue-portal')
def blue():
    return render_template_string(get_nav("#2980b9") + """
    <div style="padding:20px; font-family:sans-serif;">
        <h1>🛡 BLUE TEAM DEFENSE</h1>
        <div style="background:#e3f2fd; padding:15px; border-radius:10px;">
            <h3>Dòng lệnh Commit Vá lỗi:</h3>
            <p>Sau khi sửa code trong <b>Edit Code</b>, hãy nhấn nút xác nhận bên dưới:</p>
            <button onclick="commit('sqli')">Commit SQLi Fix</button>
            <button onclick="commit('cmd_inj')">Commit CMD Fix</button>
            <button onclick="commit('lfi')">Commit LFI Fix</button>
            <button onclick="commit('xss')">Commit XSS Fix</button>
            <button onclick="commit('broken_auth')">Commit Auth Fix</button>
        </div>
        <br><a href="/edit-code"><button style="background:#2ecc71; color:white;">⚙ VÀO TRÌNH SỬA CODE</button></a>
    </div>
    <script>
        function commit(type){
            fetch('http://192.168.102.45:5000/api/commit_fix', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({vuln_type: type})
            }).then(() => alert('Đã gửi xác nhận vá lỗi!'));
        }
    </script>
    <style>button{margin:5px; padding:10px; cursor:pointer;}</style>
    """)

# --- 5 LỖ HỔNG (SQLI, CMD, LFI, XSS, AUTH) ---
@app.route('/sqli', methods=['GET','POST'])
def sqli():
    # Giả lập code lỗi SQLi
    return "<h1>Challenge 1: SQL Injection</h1><form method='POST'><input name='u'></form>"

@app.route('/cmd')
def cmd():
    # Giả lập code lỗi CMD Inj
    return "<h1>Challenge 2: Command Injection</h1><form><input name='ip'></form>"

@app.route('/lfi')
def lfi():
    return "<h1>Challenge 3: LFI</h1><a href='/view?file=note.txt'>View Note</a>"

@app.route('/xss')
def xss():
    return "<h1>Challenge 4: XSS</h1><form><input name='msg'></form>"

@app.route('/auth-bypass')
def auth_bypass():
    return "<h1>Challenge 5: Broken Auth</h1><p>Cookie: admin=false</p>"

@app.route('/edit-code', methods=['GET', 'POST'])
def edit_code():
    if request.method == 'POST':
        with open(__file__, 'w') as f: f.write(request.form.get('code'))
        os.system("python3 vuln_web.py &")
        os._exit(0)
    with open(__file__, 'r') as f: c = f.read()
    return render_template_string("<form method='POST'><textarea name='code' style='width:100%;height:80vh'>{{c}}</textarea><button>SAVE</button></form>", c=c)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
