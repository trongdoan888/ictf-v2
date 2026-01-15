import requests
import time

# CHÚ THÍCH: Script này là "Bộ não" của giải đấu, chạy trên máy CENTRAL
# Nó sẽ kết nối tới máy Teams để kiểm tra xem dịch vụ có còn hoạt động không.

TEAM_IP = "10.10.20.10" # IP máy Teams bạn đã cấu hình
SERVICE_PORT = 8080      # Cổng dịch vụ Web của Team

def check_service():
    try:
        # Gửi request kiểm tra dịch vụ của Team
        response = requests.get(f"http://{TEAM_IP}:{SERVICE_PORT}", timeout=3)
        if response.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] Team tại {TEAM_IP}: UP (Nhận 10 điểm SLA)")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Team tại {TEAM_IP}: DOWN (Bị trừ điểm)")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Team tại {TEAM_IP}: ERROR (Không kết nối được)")

if __name__ == "__main__":
    print("--- iCTF GAMEBOT ĐANG CHẠY ---")
    while True:
        check_service()
        time.sleep(60) # Cứ mỗi 1 phút kiểm tra 1 lần (1 Round)
