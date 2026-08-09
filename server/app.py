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
from server.routes.system import system
from server.routes.dashboard import dashboard
from server.routes.running import running
from server.routes.topology import topology
from server.routes.analytics import analytics
from server.routes.analytics_data import analytics_data
from server.routes.correlation import correlation
from server.routes.matrix import matrix
from server.routes.scatter import scatter
from server.routes.cdf import cdf
from server.routes.percentile import percentile
from server.routes.latency import latency
from server.routes.compare import compare
from server.routes.statistical_compare import statistical_compare
from server.routes.research_summary import research_summary
from server.routes.topology_api import topology_api
from server.routes.live import live
from server.routes.analysis import analysis_bp
from server.routes.research.experiments import research_experiments
from server.routes.research.detail import research_detail
from server.routes.research.dashboard import research_dashboard
from server.routes.research.campaign import campaign_analysis
from server.routes.research.generator import experiment_generator
from server.routes.research.execution import experiment_execution
from server.routes.analysis_api import analysis_api



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

    app.register_blueprint(
        system,
        url_prefix="/api"
    )


    app.register_blueprint(
        dashboard
    )


    app.register_blueprint(
        analytics
    )

    app.register_blueprint(
        running
    )

    app.register_blueprint(
        analysis_bp,
        url_prefix="/api"
    )


    app.register_blueprint(
        analytics_data
    )


    app.register_blueprint(
        correlation
    )


    app.register_blueprint(
        matrix
    )


    app.register_blueprint(
        scatter
    )


    app.register_blueprint(
        cdf
    )


    app.register_blueprint(
        percentile
    )


    app.register_blueprint(
        latency
    )


    app.register_blueprint(
        compare
    )


    app.register_blueprint(
        statistical_compare
    )


    app.register_blueprint(
        research_summary
    )


    app.register_blueprint(
        research_experiments
    )


    app.register_blueprint(
        research_detail
    )


    app.register_blueprint(
        campaign_analysis
    )


    app.register_blueprint(
        experiment_generator
    )


    app.register_blueprint(
        experiment_execution
    )


    app.register_blueprint(
        research_dashboard
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
