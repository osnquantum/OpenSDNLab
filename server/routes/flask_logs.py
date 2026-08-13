from flask import Blueprint, jsonify
from pathlib import Path


flask_logs = Blueprint(
    "flask_logs",
    __name__
)


@flask_logs.route("/api/flask/logs")
def get_flask_logs():

    logs = []

    files = [
        Path("opensdn_flask.log"),
        Path("logs/application/app.log")
    ]

    for file in files:

        if file.exists():

            logs.append(
                "\n========== "
                + str(file)
                + " ==========\n"
            )

            lines = file.read_text(
                errors="ignore"
            ).splitlines()[-100:]

            logs.extend(
                line + "\n"
                for line in lines
            )

    return jsonify({
        "success": True,
        "logs": logs
    })
