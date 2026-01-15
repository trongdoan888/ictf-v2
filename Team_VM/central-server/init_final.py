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

# Import các module chức năng
from . import teams, services, general, scored_events, scores, scripts, uploads, ticket

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
