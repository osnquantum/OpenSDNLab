from flask import Blueprint,jsonify,request

from server.services.experiment_generator import ExperimentGenerator


experiment_generator = Blueprint(
    "experiment_generator",
    __name__
)


service=ExperimentGenerator()



@experiment_generator.route(
"/api/research/experiment/create",
methods=["POST"]
)

def create():


    data=request.json


    experiment_id = service.create_experiment(
        data["template_id"]
    )


    return jsonify({

        "success":True,

        "experiment_id":experiment_id

    })

