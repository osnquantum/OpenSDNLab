"""
OpenSDNLab System Orchestrator
"""

from engine.orchestration.cleanup_manager import CleanupManager
from engine.orchestration.controller_guard import ControllerGuard
from engine.orchestration.controller_runtime import ControllerRuntimeManager


class SystemManager:


    def __init__(self):

        self.cleanup_manager = CleanupManager()

        self.controller_runtime = ControllerRuntimeManager()

        self.controller_guard = ControllerGuard()



    def prepare(self, controller="osken"):


        cleanup_status = (
            self.cleanup_manager.cleanup_mininet()
        )


        controller_info = (
            self.controller_runtime.start(
                controller
            )
        )


        controller_status = (
            self.controller_guard.check()
        )


        return {

            "cleanup": cleanup_status,

            "controller": controller_status,

            "controller_info": controller_info,

            "ready":
                cleanup_status and controller_status

        }
