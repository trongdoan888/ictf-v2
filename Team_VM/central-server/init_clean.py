#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Flask
from .flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_envvar("ICTF_DATABASE_SETTINGS")
mysql = MySQL(app)

@app.route("/ping")
def ping():
    return "pong"

# Chỉ import những module gốc mà file cũ đã có
from . import brand_new_scoring
from . import db_helpers
from . import scored_events
from . import scores
from . import scripts
from . import services
from . import teams
from . import general
from . import uploads
from . import ticket

if __name__ == "__main__":
    app.run(host="0.0.0.0")
