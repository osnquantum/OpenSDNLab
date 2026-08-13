from engine.repository.sqlite.sqlite_repository import SQLiteRepository


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

        exp.topology = row[2]

        exp.hosts = row[3]

        exp.switches = row[4]

        exp.protocol = row[5]

        exp.controller = row[6]


        return exp
