from flask import Blueprint, jsonify

from server.services.campaign_analysis_service import CampaignAnalysisService



campaign_analysis = Blueprint(
    "campaign_analysis",
    __name__
)



service = CampaignAnalysisService()



@campaign_analysis.route(
    "/api/research/campaign/<group_id>",
    methods=["GET"]
)

def campaign_detail(group_id):


    result = service.analyze_campaign(
        group_id
    )


    return jsonify({

        "success":True,

        "analysis":result

    })
