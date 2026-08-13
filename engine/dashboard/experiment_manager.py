import time
import uuid


class ExperimentManager:


    def __init__(self):

        self.jobs = {}



    def create_job(self, experiment_id, runs=1):

        job_id = (
            "JOB-"
            +
            str(uuid.uuid4())[:8]
        )


        self.jobs[job_id] = {

            "job_id": job_id,

            "experiment_id":
                experiment_id,

            "total_runs":
                runs,

            "completed_runs":
                0,

            "failed_runs":
                0,

            "status":
                "CREATED",

            "created_at":
                time.time()

        }


        return self.jobs[job_id]



    def start_job(self, job_id):

        if job_id in self.jobs:

            self.jobs[job_id]["status"] = "RUNNING"


        return self.jobs.get(job_id)



    def update_run(self, job_id, success=True):

        if job_id not in self.jobs:
            return None


        if success:

            self.jobs[job_id]["completed_runs"] += 1

        else:

            self.jobs[job_id]["failed_runs"] += 1



        total = self.jobs[job_id]["total_runs"]


        completed = (
            self.jobs[job_id]["completed_runs"]
            +
            self.jobs[job_id]["failed_runs"]
        )


        if completed >= total:

            self.jobs[job_id]["status"] = "COMPLETED"



        return self.jobs[job_id]



    def get_job(self, job_id):

        return self.jobs.get(job_id)



    def get_all(self):

        return list(
            self.jobs.values()
        )
