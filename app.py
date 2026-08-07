"""
SignalSentinel AI - Flask Application
Command & Control dashboard for national/multi-city traffic management.
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from services.simulator import simulator

app = Flask(__name__)
CORS(app)


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/status")
def api_status():
    return jsonify(simulator.get_status())


@app.route("/api/heatmap")
def api_heatmap():
    return jsonify(simulator.get_heatmap())


@app.route("/api/ai/toggle", methods=["POST"])
def api_ai_toggle():
    return jsonify(simulator.toggle_ai())


@app.route("/api/ai/force-cycle", methods=["POST"])
def api_force_cycle():
    return jsonify(simulator.force_cycle())


@app.route("/api/green-wave", methods=["POST"])
def api_green_wave():
    data = request.get_json(silent=True) or {}
    route = data.get("route", "Route 7 — Central Hospital Corridor")
    return jsonify(simulator.trigger_green_wave(route))


@app.route("/api/policy/simulate", methods=["POST"])
def api_policy_sim():
    data = request.get_json(silent=True) or {}
    policy = data.get("policy", "Peak Hour Aggressive")
    return jsonify(simulator.run_policy_sim(policy))


@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "SignalSentinel AI"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
