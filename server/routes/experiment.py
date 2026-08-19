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


@experiment.route(
    "/experiments/prepare",
    methods=["POST"]
)
def prepare_experiment():

    data = request.get_json(
        silent=True
    ) or {}

    result = experiment_service.prepare_experiment(
        data
    )

    return success(
        result,
        "Experiment prepared successfully."
    )
