"""
Experiment Job Status
"""

from enum import Enum


class JobStatus(Enum):

    CREATED = "CREATED"

    QUEUED = "QUEUED"

    RUNNING = "RUNNING"

    PAUSED = "PAUSED"

    STOPPED = "STOPPED"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    ARCHIVED = "ARCHIVED"

