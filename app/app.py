"""Visitor Counter - Flask + Redis."""
import os
import socket

import redis
from flask import Flask, jsonify, render_template

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CLUSTER_NAME = os.getenv("CLUSTER_NAME", "local")  # private / public / local

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True,
                socket_connect_timeout=2, socket_timeout=2)
app = Flask(__name__)


@app.route("/")
def index():
    try:
        count = r.incr("visits")
    except redis.exceptions.RedisError:
        return "<h1>Redis unavailable</h1>", 503

    return render_template(
        "index.html",
        count=count,
        pod=socket.gethostname(),
        cluster=CLUSTER_NAME
    )


@app.route("/info")
def info():
    """Machine-friendly endpoint used by curl loops (does not touch the counter)."""
    return jsonify(cluster=CLUSTER_NAME, pod=socket.gethostname())


@app.route("/health")
def health():
    """Liveness: the process is up."""
    return "ok", 200


@app.route("/ready")
def ready():
    """Readiness: the app can reach Redis."""
    try:
        r.ping()
        return "ready", 200
    except redis.exceptions.RedisError:
        return "redis not reachable", 503


@app.route("/work")
def work():
    """CPU-heavy endpoint used only to trigger the autoscaler."""
    total = 0
    for i in range(300_000):
        total += i * i
    return jsonify(result=total, pod=socket.gethostname())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
