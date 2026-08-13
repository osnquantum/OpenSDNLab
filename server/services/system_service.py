from engine.orchestration.system_manager import SystemManager

import subprocess
from engine.repository.sqlite.sqlite_repository import SQLiteRepository



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



    def readiness(self):

        checks = {}


        # API
        checks["api"] = {
            "status": "PASS"
        }


        # Controller
        controller = self.manager.controller_guard.check()

        checks["controller"] = {

            "status":
                "PASS" if controller else "FAIL",

            "running":
                controller,

            "port":
                6653

        }


        # OVS
        try:

            result = subprocess.run(
                ["sudo","-n","ovs-vsctl","show"],
                capture_output=True,
                text=True,
                timeout=3
            )

            checks["ovs"] = {

                "status":
                    "PASS" if result.returncode == 0 else "FAIL"

            }


        except Exception as e:

            checks["ovs"] = {

                "status":"FAIL",

                "error":str(e)

            }



        # Mininet
        try:

            subprocess.run(
                ["mn","--version"],
                capture_output=True,
                timeout=3
            )

            checks["mininet"]={

                "status":"PASS"

            }


        except Exception as e:

            checks["mininet"]={

                "status":"FAIL",

                "error":str(e)

            }



        # Database

        try:

            SQLiteRepository()

            checks["database"]={

                "status":"PASS"

            }


        except Exception as e:

            checks["database"]={

                "status":"FAIL",

                "error":str(e)

            }



        ready = all(
            x["status"]=="PASS"
            for x in checks.values()
            if x["status"]!="UNKNOWN"
        )


        return {

            "ready":ready,

            "checks":checks

        }



    def status(self):

        return {

            "api": True,

            "controller":
                self.manager.controller_guard.check()

        }
