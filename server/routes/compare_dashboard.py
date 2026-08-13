from flask import Blueprint, render_template
from engine.repository.sqlite.sqlite_repository import SQLiteRepository


compare_dashboard = Blueprint(
    "compare_dashboard",
    __name__
)


db = SQLiteRepository()


@compare_dashboard.route("/compare")
def compare():

    rows = db.connection.execute(
        """
        SELECT DISTINCT experiment_id
        FROM experiment_runs
        ORDER BY experiment_id
        """
    ).fetchall()


    experiments = [
        r[0] for r in rows
    ]


    return render_template(
        "compare.html",
        experiments=experiments
    )
