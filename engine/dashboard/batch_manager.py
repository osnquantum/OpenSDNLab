import time


class BatchManager:


    def __init__(self):

        self.batches = {}



    def create_batch(
        self,
        job_id,
        total_runs
    ):

        self.batches[job_id] = {

            "job_id":
                job_id,

            "total_runs":
                total_runs,

            "current_run":
                0,

            "successful":
                0,

            "failed":
                0,

            "status":
                "CREATED",

            "started_at":
                None

        }


        return self.batches[job_id]



    def start_batch(self, job_id):

        if job_id in self.batches:

            self.batches[job_id]["status"] = "RUNNING"

            self.batches[job_id]["started_at"] = time.time()


        return self.batches.get(job_id)



    def update_progress(
        self,
        job_id,
        success=True
    ):

        batch = self.batches.get(job_id)


        if not batch:
            return None



        batch["current_run"] += 1


        if success:

            batch["successful"] += 1

        else:

            batch["failed"] += 1



        if batch["current_run"] >= batch["total_runs"]:

            batch["status"] = "COMPLETED"



        return batch



    def get_status(self, job_id):

        return self.batches.get(job_id)



    def get_all(self):

        return list(
            self.batches.values()
        )
