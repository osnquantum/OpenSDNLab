from engine.repository.sqlite.sqlite_repository import SQLiteRepository
import json


class ExperimentLoader:


    def __init__(self):

        self.db = SQLiteRepository()



    def load(self, experiment_id):


        cursor = self.db.connection.cursor()


        cursor.execute(
            """
            SELECT

            experiment_id,
            experiment_name,
            topology,
            topology_data,
            hosts,
            switches,
            protocol,
            controller

            FROM experiments

            WHERE experiment_id=?

            """,
            (experiment_id,)
        )


        row = cursor.fetchone()


        if not row:

            return None



        class Experiment:
            pass



        exp = Experiment()


        exp.experiment_id = row[0]

        exp.experiment_name = row[1]

        # Preserve the complete custom topology when available.
        if row[3]:
            try:
                exp.topology_data = json.loads(row[3])
            except (TypeError, json.JSONDecodeError):
                exp.topology_data = {
                    "type": row[2],
                    "hosts": row[4],
                    "switches": row[5]
                }
        else:
            exp.topology_data = {
                "type": row[2],
                "hosts": row[4],
                "switches": row[5]
            }

        exp.topology = row[2]

        exp.hosts = row[4]

        exp.switches = row[5]

        exp.protocol = row[6]

        exp.controller = row[7]


        return exp
