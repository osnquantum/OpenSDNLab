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

    def get_results(self, job_id):

        import statistics

        job = self.database.connection.execute(
            """
            SELECT
                job_id,
                experiment_id,
                total_runs,
                current_run,
                successful,
                failed,
                status,
                created_at,
                started_at
            FROM batch_jobs
            WHERE job_id=?
            """,
            (job_id,)
        ).fetchone()

        if not job:
            return None

        rows = self.database.connection.execute(
            """
            SELECT
                run_number,
                minimum_rtt,
                average_rtt,
                maximum_rtt,
                jitter,
                packet_loss,
                throughput,
                estimated_one_way_delay,
                mos,
                created_at
            FROM experiment_runs
            WHERE job_id=?
            ORDER BY run_number
            """,
            (job_id,)
        ).fetchall()

        runs = []

        for row in rows:

            runs.append({

                "run_number": row[0],
                "minimum_rtt": row[1],
                "average_rtt": row[2],
                "maximum_rtt": row[3],
                "jitter": row[4],
                "packet_loss": row[5],
                "throughput": row[6],
                "one_way_delay": row[7],
                "mos": row[8],
                "created_at": row[9]

            })

        metrics = [
            "minimum_rtt",
            "average_rtt",
            "maximum_rtt",
            "jitter",
            "packet_loss",
            "throughput",
            "one_way_delay",
            "mos"
        ]

        statistics_result = {}

        for metric in metrics:

            values = [
                run[metric]
                for run in runs
                if run[metric] is not None
            ]

            if not values:
                continue

            statistics_result[metric] = {

                "mean":
                    round(
                        statistics.mean(values),
                        4
                    ),

                "minimum":
                    round(
                        min(values),
                        4
                    ),

                "maximum":
                    round(
                        max(values),
                        4
                    ),

                "stddev":
                    round(
                        statistics.stdev(values),
                        4
                    )
                    if len(values) > 1
                    else 0.0

            }

        # ------------------------------------------------------------
        # QoS / QoE decisions for this batch
        # ------------------------------------------------------------

        decisions_rows = self.database.connection.execute(
            """
            SELECT
                run_number,
                action,
                reason,
                created_at
            FROM qos_qoe_decisions
            WHERE experiment_id=?
              AND run_number IN (
                  SELECT run_number
                  FROM experiment_runs
                  WHERE job_id=?
              )
            ORDER BY run_number
            """,
            (
                job[1],
                job_id
            )
        ).fetchall()

        decisions = []

        for row in decisions_rows:

            decisions.append({
                "run_number": row[0],
                "action": row[1],
                "reason": row[2],
                "created_at": row[3]
            })


        # ------------------------------------------------------------
        # Controller metrics for this batch
        # ------------------------------------------------------------

        controller_rows = self.database.connection.execute(
            """
            SELECT
                run_number,
                controller_id,
                metric_name,
                metric_value,
                created_at
            FROM controller_metrics
            WHERE experiment_id=?
              AND run_number IN (
                  SELECT run_number
                  FROM experiment_runs
                  WHERE job_id=?
              )
            ORDER BY run_number, id
            """,
            (
                job[1],
                job_id
            )
        ).fetchall()

        controller_metrics = []

        for row in controller_rows:

            controller_metrics.append({
                "run_number": row[0],
                "controller_id": row[1],
                "metric_name": row[2],
                "metric_value": row[3],
                "created_at": row[4]
            })


        # ------------------------------------------------------------
        # Pivot controller metrics into one summary row per run.
        #
        # Multiple controller snapshots may exist for a run. The
        # latest snapshot is used for the run-level summary.
        # ------------------------------------------------------------

        controller_summary_map = {}

        for item in controller_metrics:

            run_number = item["run_number"]

            if run_number not in controller_summary_map:
                controller_summary_map[run_number] = {
                    "run_number": run_number,
                    "controller_id": item["controller_id"],
                    "created_at": item["created_at"]
                }

            # Later records are newer because the query is ordered by id.
            controller_summary_map[run_number]["created_at"] = item["created_at"]

            controller_summary_map[run_number][
                item["metric_name"]
            ] = item["metric_value"]

        controller_summary = list(
            controller_summary_map.values()
        )

        controller_summary.sort(
            key=lambda item: item["run_number"]
        )

        # Display batch-relative run numbers (1..N) instead of
        # the experiment-wide database run numbers.
        for batch_index, item in enumerate(
            controller_summary,
            start=1
        ):
            item["database_run_number"] = item["run_number"]
            item["run_number"] = batch_index


        return {

            "job": {

                "job_id": job[0],
                "experiment_id": job[1],
                "total_runs": job[2],
                "current_run": job[3],
                "successful": job[4],
                "failed": job[5],
                "status": job[6],
                "created_at": job[7],
                "started_at": job[8]

            },

            "runs": runs,

            "statistics":
                statistics_result,

            "decisions":
                decisions,

            "controller_metrics":
                controller_metrics,

            "controller_summary":
                controller_summary

        }

