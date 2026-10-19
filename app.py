"""Intentionally vulnerable Flask app — test target only, never deploy."""

import sqlite3
import subprocess

import yaml
from flask import Flask, request

app = Flask(__name__)
app.secret_key = "dev-secret-key-123456"  # fake, hard-coded on purpose
DB_PASSWORD = "SuperSecret123!"  # fake, hard-coded on purpose


@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    # SQL injection: user input concatenated into the query
    rows = conn.execute("SELECT * FROM users WHERE name = '" + name + "'").fetchall()
    return {"users": rows}


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # OS command injection: user input passed to a shell
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return out


@app.route("/import", methods=["POST"])
def import_config():
    # Unsafe deserialization: yaml.load without SafeLoader
    data = yaml.load(request.data, Loader=yaml.Loader)
    return {"keys": list(data or {})}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
