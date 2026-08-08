"""
Topology Generator API
"""

from flask import Blueprint, request, jsonify


topology_api = Blueprint(
    "topology_api",
    __name__
)



@topology_api.route(
    "/api/topology/generate",
    methods=["POST"]
)
def generate():


    data = request.json


    topology = {

        "type":
        data.get("type","linear"),


        "hosts":
        int(data.get("hosts",2)),


        "switches":
        int(data.get("switches",1)),


        "controller":
        data.get("controller","ryu")

    }


    return jsonify({

        "success":True,

        "message":
        "Topology generated successfully.",

        "topology":
        topology

    })
