from flask import Flask, render_template_string, request, jsonify
import time, random, string, threading

app = Flask(__name__)
app.secret_key = "central_secret_2026"

# Quản lý Flag động (thay đổi mỗi 5 phút)
FLAGS = {"sqli": "ICTF{INIT_SQL}", "rce": "ICTF{INIT_RCE}"}
SCORES = {"Team_TrongDoan": 0}

def rotate_flags():
    while True:
        FLAGS["sqli"] = "ICTF{SQL_" + ''.join(random.choices(string.ascii_uppercase, k=8)) + "}"
        FLAGS["rce"] = "ICTF{RCE_" + ''.join(random.choices(string.ascii_uppercase, k=8)) + "}"
        time.sleep(300)

threading.Thread(target=rotate_flags, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template_string("""
    <body style="background:#0f172a; color:white; font-family:sans-serif; padding:50px;">
        <h1>CENTRAL ADMIN - SCOREBOARD</h1>
        <div style="background:#1e293b; padding:20px; border-radius:10px; border-left: 5px solid #3b82f6;">
            <h3>BẢNG ĐIỂM THỜI GIAN THỰC</h3>
            <h2 style="color:#fbbf24;">Team TrongDoan: {{ score }} ĐIỂM</h2>
        </div>
        <hr>
        <p>Hệ thống đang chạy 2 mục tiêu: <b>Cổng 5001 (SQLi)</b> và <b>Cổng 5002 (RCE)</b></p>
    </body>
    """, score=SCORES["Team_TrongDoan"])

@app.route('/submit', methods=['POST'])
def submit():
    flag = request.json.get('flag')
    if flag in FLAGS.values():
        SCORES["Team_TrongDoan"] += 500
        return jsonify({"status": "success", "msg": "Flag đúng! +500 điểm"})
    return jsonify({"status": "error", "msg": "Flag sai hoặc đã hết hạn!"})

# Các cổng bài tập mô phỏng
@app.route('/target/sqli')
def target_sqli(): return f"SQL Portal. Hint: Payload ' OR 1=1. Hidden Flag: {FLAGS['sqli']}"

@app.route('/target/rce')
def target_rce(): return f"RCE Portal. Hint: Use ; ls. Hidden Flag: {FLAGS['rce']}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
