import sqlite3
import uuid
from datetime import datetime


DB_PATH="storage/database/opensdnlab.db"


class ExperimentGenerator:


    def __init__(self):

        self.connection = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )


    def create_experiment(self, template_id):

        cursor=self.connection.cursor()


        cursor.execute(
            """
            SELECT

            name,
            objective,
            controller,
            topology,
            hosts,
            switches,
            links,
            protocol,
            traffic_type,
            bandwidth,
            delay,
            loss,
            runs,
            controller_version,
            controller_config

            FROM experiment_templates

            WHERE template_id=?

            """,
            (template_id,)
        )


        template=cursor.fetchone()


        if not template:

            return None



        experiment_id = (
            "EXP-"
            +
            datetime.now().strftime("%Y%m%d")
            +
            "-"
            +
            uuid.uuid4().hex[:6]
        )


        cursor.execute(
            """
            INSERT INTO experiments
            (

            experiment_id,
            experiment_name,
            controller,
            topology,
            hosts,
            switches,
            links,
            protocol,
            bandwidth,
            delay,
            loss,
            template_id,
            run_count,
            experiment_status,
            created_at,
            controller_version,
            controller_config

            )

            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

            """,

            (

            experiment_id,
            template[0],
            template[2],
            template[3],
            template[4],
            template[5],
            template[6],
            template[7],
            template[9],
            template[10],
            template[11],
            template_id,
            template[12],
            "created",
            datetime.now().isoformat(),
            template[13],
            template[14]

            )

        )


        self.connection.commit()


        return experiment_id
