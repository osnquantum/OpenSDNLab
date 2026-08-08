"""
Topology Builder Page
"""

from flask import Blueprint, render_template, request


topology = Blueprint(
    "topology",
    __name__
)


@topology.route("/topology")
def topology_page():

    return render_template(
        "topology.html"
    )
