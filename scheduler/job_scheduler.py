"""
Experiment Job Scheduler
"""

class JobScheduler:

    def __init__(self, queue, experiment_manager):

        self.queue = queue

        self.experiment_manager = experiment_manager

    ############################################################

    def run(self):

        results = []

        while not self.queue.empty():

            job = self.queue.pop()

            print()

            print("=" * 60)

            print(f"Executing Job #{job.id}")

            job.status = "RUNNING"

            result = self.experiment_manager.run(

                job.configuration

            )

            job.status = "COMPLETED"

            results.append(result)

        return results
