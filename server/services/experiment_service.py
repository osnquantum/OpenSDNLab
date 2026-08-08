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



            topology=data.get(
                "topology",
                default.topology
            ),


            network=data.get(
                "network",
                default.network
            ),


            controller=data.get(
                "controller",
                default.controller
            ),


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

            "status": job.status.name,

            "message": "Experiment submitted successfully."

        }



experiment_service = ExperimentService()
