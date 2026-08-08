"""
Analysis Routes

Research experiment analysis API.
"""

from flask import Blueprint, request, jsonify

from engine.analysis.service.analysis_service import AnalysisService


analysis_bp = Blueprint(
    "analysis",
    __name__
)


service = AnalysisService()



############################################################
# Get experiment summary
############################################################

@analysis_bp.route(
    "/api/analysis/experiment/<experiment_id>",
    methods=["GET"]
)
def experiment_summary(
    experiment_id
):

    result = service.get_experiment(
        experiment_id
    )


    return jsonify({

        "success": True,

        "data": result

    })



############################################################
# Compare experiments
############################################################

@analysis_bp.route(
    "/api/analysis/compare",
    methods=["GET"]
)
def compare_experiments():

    exp1 = request.args.get(
        "id1"
    )

    exp2 = request.args.get(
        "id2"
    )


    result = service.compare(
        exp1,
        exp2
    )


    return jsonify({

        "success": True,

        "data": result

    })
