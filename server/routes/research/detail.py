from flask import Blueprint, jsonify

from engine.repository.sqlite.sqlite_repository import SQLiteRepository


research_detail = Blueprint(
    "research_detail",
    __name__
)


db = SQLiteRepository()



@research_detail.route(
    "/api/research/experiment/<experiment_name>",
    methods=["GET"]
)
def experiment_detail(experiment_name):


    cursor = db.connection.cursor()



    # Experiment information

    cursor.execute(
        """
        SELECT

        experiment_name,
        experiment_name,
        topology,
        hosts,
        switches,
        links,
        protocol,
        controller,
        bandwidth,
        delay,
        loss,
        average_rtt,
        jitter,
        packet_loss,
        throughput,
        status,
        created_at,
        notes

        FROM experiments

        WHERE experiment_name=?

        """,
        (experiment_name,)
    )


    exp = cursor.fetchone()



    if not exp:

        return jsonify({

            "success":False,

            "message":"Experiment not found"

        }),404



    # Number of runs

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM experiment_runs

        WHERE experiment_id=?

        """,
        (experiment_name,)
    )


    run_count = cursor.fetchone()[0]


    # Aggregate performance from experiment runs

    cursor.execute(
        """
        SELECT

        AVG(average_rtt),
        AVG(jitter),
        AVG(packet_loss),
        AVG(throughput)

        FROM experiment_runs

        WHERE experiment_id=?

        """,
        (experiment_name,)
    )


    performance = cursor.fetchone()



    # Run-wise time series

    cursor.execute(
        """
        SELECT

        run_number,
        average_rtt,
        throughput,
        jitter,
        packet_loss

        FROM experiment_runs

        WHERE experiment_id=?

        ORDER BY run_number

        """,
        (experiment_name,)
    )


    timeseries = [

        {
            "run":row[0],
            "rtt":row[1],
            "throughput":row[2],
            "jitter":row[3],
            "packet_loss":row[4]
        }

        for row in cursor.fetchall()

    ]



    # Available metrics

    cursor.execute(
        """
        SELECT DISTINCT metric_name

        FROM metric_registry

        WHERE enabled=1

        """
    )


    metrics=[
        row[0]
        for row in cursor.fetchall()
    ]



    return jsonify({


        "success":True,


        "experiment":{


            "id":exp[0],

            "name":exp[1],


            "configuration":{


                "topology":exp[2],

                "hosts":exp[3],

                "switches":exp[4],

                "links":exp[5],

                "protocol":exp[6],

                "controller":exp[7],

                "bandwidth":exp[8],

                "delay":exp[9],

                "loss":exp[10]

            },


            "performance":{


                "average_rtt":exp[11],

                "jitter":exp[12],

                "packet_loss":exp[13],

                "throughput":exp[14]

            },


            "runs":run_count,

              "timeseries":timeseries,


            "metrics_available":metrics,


            "status":exp[15],

            "created_at":exp[16],

            "notes":exp[17]


        }


    })
