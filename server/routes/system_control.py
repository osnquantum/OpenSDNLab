from flask import Blueprint, render_template


system_control = Blueprint(
    "system_control",
    __name__
)


@system_control.route(
    "/system-control"
)
def page():

    return render_template(
        "system/control.html"
    )
