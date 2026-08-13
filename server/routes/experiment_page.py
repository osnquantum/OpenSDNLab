from flask import Blueprint, render_template

experiment_page = Blueprint(
    "experiment_page",
    __name__
)

@experiment_page.route("/experiments")
def experiments():
    return render_template(
        "experiment_create.html"
    )
