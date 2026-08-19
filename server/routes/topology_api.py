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

    topology_type = data.get("type", "linear")
    hosts = int(data.get("hosts", 2))
    switches = int(data.get("switches", 1))
    controller = data.get("controller", "os-ken")


    nodes = []
    links = []


    # Create hosts
    for i in range(1, hosts + 1):
        nodes.append({
            "id": f"h{i}",
            "type": "host"
        })


    # Create switches
    for i in range(1, switches + 1):
        nodes.append({
            "id": f"s{i}",
            "type": "switch"
        })


    # Linear host-switch mapping
    for i in range(1, hosts + 1):

        switch_id = min(
            ((i - 1) // max(1, hosts // switches)) + 1,
            switches
        )

        links.append({
            "source": f"h{i}",
            "target": f"s{switch_id}"
        })


    # Switch-to-switch links
    for i in range(1, switches):

        links.append({
            "source": f"s{i}",
            "target": f"s{i+1}"
        })


    topology = {

        "type": topology_type,

        "hosts": hosts,

        "switches": switches,

        "controller": controller,

        "nodes": nodes,

        "links": links

    }


    return jsonify({

        "success": True,

        "message":
        "Topology graph generated successfully.",

        "topology": topology

    })
