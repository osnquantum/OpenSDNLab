from flask import Blueprint, jsonify

health = Blueprint("health", __name__)


@health.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "project": "OpenSDNLab",
        "status": "running",
        "version": "2.0.0",
        "engine": "OpenSDNLab Engine"
    })
