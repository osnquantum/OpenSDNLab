from flask import Blueprint, jsonify

from engine.analysis.service.experiment_analysis_service import (
    ExperimentAnalysisService
)


analysis_api = Blueprint(
    "analysis_api",
    __name__
)


service = ExperimentAnalysisService()



@analysis_api.route(
    "/api/analysis/experiment/<experiment_id>",
    methods=["GET"]
)
def experiment_analysis(experiment_id):

    result = service.analyze(
        experiment_id
    )

    return jsonify(result)
