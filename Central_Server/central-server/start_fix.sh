#!/bin/bash
service nginx start
service mysql start
export ICTF_DATABASE_SETTINGS=/opt/ictf/settings/database-api.py
export PYTHONPATH=/opt/ictf/database
# Thêm --host=0.0.0.0 để container khác có thể kết nối tới
/opt/ictf/venv/database/bin/python3 -m api.__init__ --host=0.0.0.0
