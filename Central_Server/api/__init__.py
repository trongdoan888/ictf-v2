from .core import app, mysql
from . import general, teams, services, scored_events, scores, scripts, uploads, ticket

@app.route("/ping")
def ping_internal():
    return "pong"
