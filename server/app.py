"""
OpenSDNLab Flask Server
"""

import os

from flask import Flask
from server.routes.job import job
from server.routes.health import health
from server.routes.capabilities import capabilities
from server.routes.jobs import jobs
from server.routes.experiment import experiment


def create_app():

    app = Flask(__name__)

    ############################################################
    # Register API Blueprints
    ############################################################

    app.register_blueprint(
        health,
        url_prefix="/api"
    )

    app.register_blueprint(
        capabilities,
        url_prefix="/api"
    )

    app.register_blueprint(
        jobs,
        url_prefix="/api"
    )

    app.register_blueprint(
        experiment,
        url_prefix="/api"
    )
    app.register_blueprint(
        job,
        url_prefix="/api"
    )

    return app


app = create_app()


if __name__ == "__main__":

    ############################################################
    # Free port 8000 if already in use
    ############################################################

    os.system("fuser -k 8000/tcp >/dev/null 2>&1")

    ############################################################
    # Start Flask Server
    ############################################################

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        use_reloader=False
    )
