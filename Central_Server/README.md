# ictf - Infrastructure for Capture The Flag Lab

Dự án này chứa toàn bộ cấu hình hạ tầng mạng và mã nguồn cho bài Lab CTF (ictf). Hệ thống bao gồm 3 phân vùng mạng được kết nối an toàn qua VPN và định tuyến qua máy Router.

## 🏗 Sơ đồ hệ thống (Topology)
- **Central Server (10.0.0.2)**: Chứa các thử thách (Docker) và VPN Server.
- **Router (10.1.0.1)**: Cầu nối giữa mạng Team và mạng Server, thực hiện NAT và VPN Client.
- **ictf-team (10.1.0.10)**: Máy của người chơi, truy cập thử thách thông qua Gateway Router.

---

## 📂 Cấu trúc thư mục
- `/central-server`: Cấu hình Docker Compose và các dịch vụ web thử thách.
- `/router`: File cấu hình OpenVPN Client (`client.conf`) và thiết lập IP Forwarding.
- `/ictf-team`: File cấu hình Netplan (`01-network-manager-all.yaml`) để thiết lập IP tĩnh và Routing.

---

## 🚀 Hướng dẫn triển khai nhanh

### 1. Trên máy Central Server
```bash
# Khởi động các dịch vụ thử thách
cd central-server
sudo docker-compose up -d
