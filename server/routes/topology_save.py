"""
Topology Save API
"""

from flask import Blueprint, request, jsonify


topology_save = Blueprint(
    "topology_save",
    __name__
)


saved_topologies = {}



@topology_save.route(
    "/api/topology/save",
    methods=["POST"]
)
def save_topology():

    data = request.json


    topology_id = data.get(
        "name",
        "custom_topology"
    )


    saved_topologies[topology_id] = data


    return jsonify({

        "success": True,

        "message":
        "Topology saved",

        "topology_id":
        topology_id,

        "data":
        data

    })
