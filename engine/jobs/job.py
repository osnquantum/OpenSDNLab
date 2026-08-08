"""
Experiment Job
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4

from engine.jobs.job_status import JobStatus


@dataclass
class Job:


    ############################################################
    # Identity
    ############################################################

    id: str = field(
        default_factory=lambda: str(uuid4())
    )

    name: str = "Experiment"


    ############################################################
    # Status
    ############################################################

    status: JobStatus = JobStatus.CREATED

    progress: float = 0.0


    ############################################################
    # Configuration
    ############################################################

    configuration: object = None


    ############################################################
    # Result
    ############################################################

    result: object = None


    ############################################################
    # Logs
    ############################################################

    logs: list = field(
        default_factory=list
    )


    ############################################################
    # Timing
    ############################################################

    created_at: datetime = field(
        default_factory=datetime.now
    )

    started_at: datetime | None = None

    finished_at: datetime | None = None


    ############################################################

    def add_log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.logs.append(
            f"[{timestamp}] {message}"
        )


    ############################################################
    # Progress Tracking
    ############################################################

    def update_progress(
        self,
        value,
        message=None
    ):

        self.progress = value

        if message:

            self.add_log(
                message
            )
