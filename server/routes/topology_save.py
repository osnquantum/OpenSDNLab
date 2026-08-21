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


# ------------------------------------------------------------
# List saved topologies
# ------------------------------------------------------------


# ------------------------------------------------------------
# List / search saved topologies
# ------------------------------------------------------------

@topology_save.route(
    "/api/topologies",
    methods=["GET"]
)
def list_topologies():

    search = (
        request.args.get(
            "search",
            ""
        )
        .strip()
        .lower()
    )


    try:

        limit = int(
            request.args.get(
                "limit",
                10
            )
        )

    except ValueError:

        limit = 10


    # Safety limits.
    limit = max(
        1,
        min(limit, 100)
    )


    topologies = []


    # Newest files first.
    files = sorted(
        TOPOLOGY_DIR.glob("*.json"),
        key=lambda path: path.stat().st_mtime,
        reverse=True
    )


    for file_path in files:

        try:

            with file_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                topology = json.load(file)


            name = topology.get(
                "name",
                "Unnamed Topology"
            )


            # Search all saved topologies by name.
            if (
                search and
                search not in name.lower()
            ):

                continue


            # Return metadata only.
            topologies.append({

                "topology_id":
                    topology.get(
                        "topology_id"
                    ),

                "name":
                    name,

                "type":
                    topology.get(
                        "type",
                        "custom"
                    ),

                "controller":
                    topology.get(
                        "controller",
                        "unknown"
                    ),

                "nodes":
                    len(
                        topology.get(
                            "nodes",
                            []
                        )
                    ),

                "links":
                    len(
                        topology.get(
                            "links",
                            []
                        )
                    ),

                "created_at":
                    file_path.stat().st_mtime

            })


            # Stop reading once we have enough results.
            if len(topologies) >= limit:

                break


        except Exception as error:

            print(
                "Failed to read topology:",
                file_path,
                error
            )


    return jsonify({

        "success": True,

        "search":
            search,

        "limit":
            limit,

        "count":
            len(topologies),

        "data":
            topologies

    })

