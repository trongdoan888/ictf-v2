from flask import Flask
from .flaskext.mysql import MySQL

app = Flask(__name__)
app.config.from_envvar('ICTF_DATABASE_SETTINGS')
mysql = MySQL(app)
