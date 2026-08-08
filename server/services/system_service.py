from engine.orchestration.system_manager import SystemManager


class SystemService:


    def __init__(self):

        self.manager = SystemManager()



    def start(self):

        result = self.manager.prepare(
            controller="osken"
        )

        return {
            "status": "ready",
            "data": result
        }



    def stop(self):

        self.manager.controller_runtime.stop()

        return {
            "status": "stopped"
        }



    def restart(self):

        self.manager.controller_runtime.stop()

        result = self.manager.prepare(
            controller="osken"
        )

        return {
            "status": "restarted",
            "data": result
        }



    def status(self):

        return {

            "api": True,

            "controller":
                self.manager.controller_guard.check()

        }
