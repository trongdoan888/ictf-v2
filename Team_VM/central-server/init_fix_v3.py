#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from .flaskext.mysql import MySQL
import sys

app = Flask(__name__)
app.config.from_envvar("ICTF_DATABASE_SETTINGS")
mysql = MySQL(app)

@app.route("/ping")
def ping():
    return "pong"

# Đưa việc import vào trong một hàm hoặc để ở cuối cùng sau khi app/mysql đã sẵn sàng
with app.app_context():
    from . import teams
    from . import services
    from . import general
    from . import scored_events
    from . import scores
    from . import scripts
    from . import uploads
    from . import ticket

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
