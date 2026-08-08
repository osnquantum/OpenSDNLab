"""
Research Analytics Routes
"""

from flask import Blueprint, render_template

from server.services.analytics_service import AnalyticsService


analytics = Blueprint(
    "analytics",
    __name__
)


service = AnalyticsService()



@analytics.route(
    "/analytics/<experiment_name>"
)
def analytics_page(experiment_name):

    data = service.experiment_analysis(
        experiment_name
    )


    return render_template(
        "analytics.html",
        data=data,
        experiment_name=experiment_name
    )
