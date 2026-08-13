import time


class BatchRepository:


    def __init__(self, database):

        self.database = database



    def create(
        self,
        job_id,
        experiment_id,
        runs
    ):

        self.database.connection.execute(
            """
            INSERT INTO batch_jobs
            (
                job_id,
                experiment_id,
                total_runs,
                status,
                created_at
            )

            VALUES
            (?,?,?,?,?)
            """,
            (
                job_id,
                experiment_id,
                runs,
                "CREATED",
                time.time()
            )
        )


        self.database.connection.commit()



    def update(
        self,
        job_id,
        **kwargs
    ):

        fields = []

        values = []


        for k,v in kwargs.items():

            fields.append(
                f"{k}=?"
            )

            values.append(v)



        values.append(job_id)


        query = (
            "UPDATE batch_jobs SET "
            +
            ",".join(fields)
            +
            " WHERE job_id=?"
        )


        self.database.connection.execute(
            query,
            values
        )

        self.database.connection.commit()



    def get(self, job_id):

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM batch_jobs
            WHERE job_id=?
            """,
            (job_id,)
        )


        row = cursor.fetchone()


        if not row:

            return None


        return {

            "job_id": row[1],

            "experiment_id": row[2],

            "total_runs": row[3],

            "current_run": row[4],

            "successful": row[5],

            "failed": row[6],

            "status": row[7]

        }
