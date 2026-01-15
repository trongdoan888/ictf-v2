#!/bin/bash
service nginx start
# Chạy uwsgi trực tiếp bằng module python3 để tránh lỗi "command not found"
uwsgi --http :5000 --manage-script-name --mount /api=app:app --enable-threads
