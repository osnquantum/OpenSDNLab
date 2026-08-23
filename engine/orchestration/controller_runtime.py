"""
Legacy Controller Runtime Manager

Controller lifecycle is handled by:

    ExperimentExecutor
        -> ControllerManager
        -> OsKenController

This compatibility class remains only so older code importing
ControllerRuntimeManager does not start a second OS-Ken process.
"""

from engine.core.logger import logger


class ControllerRuntimeManager:

    def __init__(self):

        self.controller_name = None


    def start(self, controller_name="osken"):

        self.controller_name = controller_name

        logger.info(
            "ControllerRuntimeManager is disabled. "
            "Controller lifecycle is managed by ControllerManager."
        )

        return {
            "controller": controller_name,
            "managed_by": "ControllerManager",
            "started": False
        }


    def stop(self):

        logger.info(
            "ControllerRuntimeManager stop ignored. "
            "Controller lifecycle is managed by ControllerManager."
        )

        return True


    def status(self):

        return {
            "controller": self.controller_name,
            "running": False,
            "managed_by": "ControllerManager"
        }
