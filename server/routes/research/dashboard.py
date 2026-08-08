from flask import Blueprint, render_template


research_dashboard = Blueprint(
    "research_dashboard",
    __name__
)


@research_dashboard.route("/research")
def research_page():

    return render_template(
        "research/dashboard.html"
    )
