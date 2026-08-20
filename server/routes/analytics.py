"""
Research Analytics Routes
"""

from flask import Blueprint, render_template, request

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

    job_id = request.args.get("job_id")

    data = service.experiment_analysis(
        experiment_name,
        job_id=job_id
    )


    return render_template(
        "analytics.html",
        data=data,
        experiment_name=experiment_name,
        job_id=job_id
    )
