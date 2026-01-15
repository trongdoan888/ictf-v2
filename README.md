# 🏆 iCTF 2026 - Hạ tầng diễn tập chuyên nghiệp

Dự án này chứa toàn bộ mã nguồn và cấu hình mạng cho Lab iCTF 3 máy ảo.

## 📁 Cấu trúc
- `/Central_Server`: Scoreboard & API điều phối.
- `/Team_VM`: Máy mục tiêu chứa 5 lỗ hổng bảo mật.
- `/Router_Config`: Cấu hình NAT/Gateway để thông mạng nội bộ ra Internet.

## 🛠 Cách chạy
1. **Router**: Chạy file `setup_network.sh` trong thư mục `Router_Config`.
2. **Máy thật (Host)**: Chạy CMD Admin: `route add 10.10.10.0 mask 255.255.255.0 192.168.102.42`.
3. **Chạy Web**:
   - Máy Trung tâm: `python3 Central_Server/ictf_final_web.py`
   - Máy TeamVM: `sudo python3 Team_VM/vuln_web.py`
