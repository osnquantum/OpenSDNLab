"""
Dashboard Routes
"""

from flask import Blueprint, render_template

from server.services.dashboard_service import DashboardService


dashboard = Blueprint(
    "dashboard",
    __name__
)


service = DashboardService()


@dashboard.route("/")
def home():

    data = service.get_dashboard_data()

    return render_template(
        "dashboard.html",
        data=data
    )


@dashboard.route("/experiment")
def experiment():

    return render_template(
        "experiment_create.html"
    )


@dashboard.route("/topology")
def topology():

    return render_template(
        "topology.html"
    )


@dashboard.route("/analytics")
def analytics():

    return render_template(
        "analytics.html"
    )
