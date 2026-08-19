"""
Persistent Topology Save API
"""

from flask import Blueprint, request, jsonify
from pathlib import Path
from uuid import uuid4
import json


topology_save = Blueprint(
    "topology_save",
    __name__
)


# ------------------------------------------------------------
# Storage
# ------------------------------------------------------------

TOPOLOGY_DIR = Path(
    __file__
).resolve().parents[2] / "saved_topologies"

TOPOLOGY_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# Save topology
# ------------------------------------------------------------

@topology_save.route(
    "/api/topology/save",
    methods=["POST"]
)
def save_topology():

    data = request.get_json(
        silent=True
    ) or {}

    topology_id = (
        "topology-" +
        str(uuid4())
    )

    topology = {

        "topology_id":
            topology_id,

        "name":
            data.get(
                "name",
                "custom_topology"
            ),

        "type":
            data.get(
                "type",
                "custom"
            ),

        "controller":
            data.get(
                "controller",
                "osken"
            ),

        "nodes":
            data.get(
                "nodes",
                []
            ),

        "links":
            data.get(
                "links",
                []
            )
    }


    file_path = (
        TOPOLOGY_DIR /
        f"{topology_id}.json"
    )


    with file_path.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            topology,
            file,
            indent=2
        )


    return jsonify({

        "success": True,

        "message":
            "Topology saved successfully.",

        "topology_id":
            topology_id,

        "data":
            topology

    })


# ------------------------------------------------------------
# Load topology
# ------------------------------------------------------------

@topology_save.route(
    "/api/topology/<topology_id>",
    methods=["GET"]
)
def get_topology(topology_id):

    file_path = (
        TOPOLOGY_DIR /
        f"{topology_id}.json"
    )


    if not file_path.exists():

        return jsonify({

            "success": False,

            "message":
                "Topology not found."

        }), 404


    with file_path.open(
        "r",
        encoding="utf-8"
    ) as file:

        topology = json.load(file)


    return jsonify({

        "success": True,

        "data":
            topology

    })
