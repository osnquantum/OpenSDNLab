"""
Experiment API
"""

from flask import Blueprint, request

from server.services.experiment_service import experiment_service
from server.utils.api_response import success


experiment = Blueprint(
    "experiment",
    __name__
)


@experiment.route(
    "/experiments/run",
    methods=["POST"]
)
def run_experiment():

    data = request.get_json()

    result = experiment_service.run_experiment(
        data
    )

    return success(
        result,
        "Experiment completed successfully."
    )
