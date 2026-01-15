FROM ictf_base

# 1. Cài đặt các thư viện hệ thống và uwsgi trực tiếp qua apt để đảm bảo ổn định
RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y python3-pip nginx build-essential python3-dev uwsgi uwsgi-plugin-python3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/ictf/teaminterface

# 2. Copy code và các file cấu hình
COPY ./teaminterface /opt/ictf/teaminterface
COPY ./secrets /opt/ictf/secrets
COPY ./teaminterface/requirements.txt .

# 3. Cài đặt các thư viện Python còn lại
RUN pip3 install --no-cache-dir -r requirements.txt

# 4. Chạy Ansible (vẫn giữ || true để đảm bảo quá trình build không bị ngắt quãng)
RUN ansible-playbook provisioning/hephaestus_provisioning/ansible-provisioning.yml --connection=local || true

# 5. Khởi động (Thay đổi cách gọi uwsgi để không bị lỗi module)
RUN chmod +x ./start.sh
# Sử dụng trực tiếp uwsgi binary với plugin python3
# Chú ý: Chúng ta trỏ chính xác vào file wsgi.py nằm trong thư mục teaminterface
ENTRYPOINT ["/bin/bash", "-c", "service nginx start && uwsgi --http :5000 --chdir /opt/ictf/teaminterface --module teaminterface.wsgi:application"]
