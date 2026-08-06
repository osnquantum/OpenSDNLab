from scheduler.job import Job
from scheduler.job_queue import JobQueue
from scheduler.job_scheduler import JobScheduler

from models.experiment_configuration import ExperimentConfiguration


class DummyManager:

    def run(self, configuration):

        print("Running:", configuration.metadata)

        return configuration.metadata


queue = JobQueue()

for i, delay in enumerate(

    [

        "1ms",

        "5ms",

        "10ms"

    ],

    start=1

):

    config = ExperimentConfiguration(

        name="Delay"

    )

    config.metadata["delay"] = delay

    queue.push(

        Job(

            id=i,

            configuration=config

        )

    )


scheduler = JobScheduler(

    queue,

    DummyManager()

)

results = scheduler.run()

print()

print(results)
