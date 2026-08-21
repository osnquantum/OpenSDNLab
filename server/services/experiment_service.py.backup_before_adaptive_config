"""
Experiment Service
Connects Flask API with OpenSDNLab Engine
"""

from engine.models.experiment_configuration import ExperimentConfiguration
from engine.services.experiment_manager import ExperimentManager

from engine.jobs.job import Job
from engine.jobs.job_executor import job_executor


class ExperimentService:

    def __init__(self):

        self.manager = ExperimentManager()


    ############################################################

    def default_config(self):

        return ExperimentConfiguration(
            name="default"
        )


    ############################################################

    def prepare_experiment(self, data):

        default = self.default_config()

        config = ExperimentConfiguration(

            name=data.get(
                "name",
                "Batch Experiment"
            ),

            runs=data.get(
                "runs",
                1
            ),

            topology=(
                data.get("topology_data")
                if isinstance(
                    data.get("topology_data"),
                    dict
                )
                else {
                    "type": data.get(
                        "topology",
                        "custom"
                    ),
                    "hosts": data.get(
                        "hosts",
                        2
                    ),
                    "switches": data.get(
                        "switches",
                        1
                    )
                }
            ),

            network={
                "protocol":
                    data.get(
                        "protocol",
                        "ipv4"
                    )
            },

            controller={
                "type": "remote",
                "name": data.get(
                    "controller",
                    "osken"
                ),
                "ip": "127.0.0.1",
                "port": 6653
            },

            deployment=data.get(
                "deployment",
                default.deployment
            ),

            monitoring=data.get(
                "monitoring",
                default.monitoring
            ),

            variables=data.get(
                "variables",
                default.variables
            ),

            metadata=data.get(
                "metadata",
                default.metadata
            )
        )

        # Generate a lightweight job so the existing
        # ExperimentManager registers the experiment.
        job = Job(
            name=config.name,
            configuration=config
        )

        # Register metadata without starting Mininet.
        experiment_id = self.manager.prepare(
            config,
            job
        )

        return {
            "experiment_id": experiment_id,
            "message": "Experiment prepared successfully."
        }


    ############################################################

    def run_experiment(self, data):

        default = self.default_config()


        config = ExperimentConfiguration(

            name=data.get(
                "name",
                "Web Experiment"
            ),

            runs=data.get(
                "runs",
                default.runs
            ),



            topology=(
                data.get("topology_data")
                if isinstance(data.get("topology_data"), dict)
                else {
                    "type": data.get("topology", "linear"),
                    "hosts": data.get("hosts", 2),
                    "switches": data.get("switches", 1)
                }
            ),


            network={
                "protocol": data.get("protocol", "ipv4")
            },


            controller={
                "type": "remote",
                "name": data.get("controller", "osken"),
                "ip": "127.0.0.1",
                "port": 6653
            },


            deployment=data.get(
                "deployment",
                default.deployment
            ),


            monitoring=data.get(
                "monitoring",
                default.monitoring
            ),


            variables=data.get(
                "variables",
                default.variables
            ),


            metadata=data.get(
                "metadata",
                default.metadata
            )
        )


        ############################################################
        # Create background job
        ############################################################

        job = Job(

            name=config.name,

            configuration=config

        )


        job_executor.job_manager.submit(
            job
        )


        job_executor.execute(

            job,

            self.manager

        )


        return {

            "job_id": job.id,

            "experiment_id":
                getattr(job, "experiment_id", None),

            "status": job.status.name,

            "message": "Experiment submitted successfully."

        }



experiment_service = ExperimentService()
