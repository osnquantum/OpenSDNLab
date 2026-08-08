from flask import Blueprint, request, jsonify

from server.services.research_summary_service import ResearchSummaryService
from server.services.comparison_service import ComparisonService
from server.services.statistical_service import StatisticalService

from server.routes.compare import get_experiment_data



research_summary = Blueprint(
    "research_summary",
    __name__
)


service = ResearchSummaryService()



@research_summary.route(
"/api/analytics/research_summary",
methods=["POST"]
)
def summary():


    body=request.json


    a=body["experiment_a"]

    b=body["experiment_b"]



    data_a=get_experiment_data(a)

    data_b=get_experiment_data(b)



    comparison = ComparisonService().summarize(
        data_a,
        data_b
    )


    statistics = StatisticalService().analyze(
        data_a["rtt"],
        data_b["rtt"]
    )


    result=service.generate(
        comparison,
        statistics
    )


    return jsonify({

        "success":True,

        "experiment_a":a,

        "experiment_b":b,

        "summary":result

    })
