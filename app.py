"""Fixed version of the test app — same features, without the vulnerabilities."""

import ipaddress
import os
import sqlite3
import subprocess

import yaml
from flask import Flask, abort, request

app = Flask(__name__)
# Secrets come from the environment, never from source code.
app.secret_key = os.environ["FLASK_SECRET_KEY"]
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    # Parameterized query: the driver escapes the value
    rows = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchall()
    return {"users": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    try:
        ipaddress.ip_address(host)  # only accept a literal IP address
    except ValueError:
        abort(400, "host must be an IP address")
    # No shell, arguments passed as a list
    out = subprocess.check_output(["ping", "-c", "1", host], timeout=5)
    return out


@app.route("/import", methods=["POST"])
def import_config():
    # safe_load only builds plain Python types
    data = yaml.safe_load(request.data)
    return {"keys": list(data or {})}


if __name__ == "__main__":
    app.run(host="127.0.0.1", debug=False)
