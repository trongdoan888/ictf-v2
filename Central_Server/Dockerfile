FROM python:3.9-slim

# Cài đặt các thư viện hệ thống cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    mariadb-client \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt Flask và các thư viện Python
RUN pip install flask flask-cors requests

# Thư mục làm việc
WORKDIR /opt/ictf/gamebot

# Copy file web vào container
COPY ictf_final_web.py .

# Chạy ứng dụng
CMD ["python", "ictf_final_web.py"]
