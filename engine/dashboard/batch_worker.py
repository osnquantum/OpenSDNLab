import threading

from engine.dashboard.experiment_loader import ExperimentLoader



class BatchWorker:


    def __init__(
        self,
        batch_executor
    ):

        self.batch_executor = batch_executor

        self.loader = ExperimentLoader()



    def start(
        self,
        job_id,
        experiment_id,
        runs
    ):


        thread = threading.Thread(

            target=self.run,

            args=(
                job_id,
                experiment_id,
                runs
            ),

            daemon=True

        )


        thread.start()


        return {

            "started": True,

            "job_id": job_id

        }



    def run(
        self,
        job_id,
        experiment_id,
        runs
    ):


        experiment = self.loader.load(
            experiment_id
        )


        if not experiment:

            return



        self.batch_executor.run_batch(

            job_id,

            experiment,

            runs

        )
