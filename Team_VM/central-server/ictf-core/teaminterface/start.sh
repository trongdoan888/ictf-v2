#!/bin/bash
service nginx start
# Gọi uwsgi bằng module python3 để vượt qua lỗi PATH
uwsgi --http :5000 --manage-script-name --mount /api=app:app --enable-threads
