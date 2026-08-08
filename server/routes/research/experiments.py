from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


research_experiments = Blueprint(
    "research_experiments",
    __name__
)


db = SQLiteRepository()



@research_experiments.route(
    "/api/research/experiments",
    methods=["GET"]
)

def list_experiments():


    cursor = db.connection.cursor()


    cursor.execute(
        """
        SELECT

        experiment_id,
        experiment_name,
        controller,
        topology,
        hosts,
        switches,
        protocol,
        status,
        created_at,
        controller_version,
        controller_config

        FROM experiments

        ORDER BY created_at DESC

        """
    )


    rows = cursor.fetchall()


    experiments=[]


    for r in rows:


        # Aggregate real metrics from experiment runs

        cursor.execute(
            """
            SELECT

            AVG(throughput),
            AVG(average_rtt),
            AVG(jitter),
            AVG(packet_loss)

            FROM experiment_runs

            WHERE experiment_id=?

            """,
            (r[0],)
        )


        metric = cursor.fetchone()



        experiments.append({

            "experiment_id": r[0],

            "name": r[1],

            "controller": {
                "name": r[2],
                "version": r[9] if len(r) > 9 else None,
                "config": r[10] if len(r) > 10 else None
            },

            "topology": r[3],

            "hosts": r[4],

            "switches": r[5],

            "protocol": r[6],


            "metrics":{

                "throughput": metric[0],

                "rtt": metric[1],

                "jitter": metric[2],

                "packet_loss": metric[3]

            },


            "status": r[7],

            "created_at": r[8]

        })



    return jsonify({

        "success": True,

        "count": len(experiments),

        "experiments": experiments

    })
