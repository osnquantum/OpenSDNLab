import subprocess
import os
import signal
import time

from engine.controllers.base_controller import BaseController
from engine.controllers.controller_logger import ControllerLogger


class OsKenController(BaseController):


    def __init__(self):

        self.process = None
        self.port = 6653
        self.start_time = None


    def start(self):

        ControllerLogger.add(
            "OSKen start requested"
        )

        self.stop()

        ControllerLogger.add(
            "Launching OSKen controller process"
        )

        self.process = subprocess.Popen(
            [
                "osken-manager",
                "engine.controllers.apps.simple_switch_13"
            ],
            stdout=open(
                "logs/osken.log",
                "w"
            ),
            stderr=subprocess.STDOUT
        )

        self.start_time = time.time()


        ControllerLogger.add(
            f"OSKen started PID={self.process.pid}"
        )


        return {

            "controller": self.name(),

            "pid": self.process.pid,

            "port": self.port,

            "running": True

        }


    def stop(self):

        if self.process:

            ControllerLogger.add(
                f"Stopping OSKen PID={self.process.pid}"
            )


            try:

                os.kill(
                    self.process.pid,
                    signal.SIGTERM
                )

            except ProcessLookupError:

                pass


            self.process = None
            self.start_time = None


            ControllerLogger.add(
                "OSKen stopped"
            )


        return True


    def status(self):

        running = False
        pid = None


        result = subprocess.getoutput(
            "pgrep -f 'osken-manager'"
        )


        if result.strip():

            running = True

            pid = result.split("\n")[0]


        uptime = None

        if running and self.start_time:

            uptime = round(
                time.time() - self.start_time,
                2
            )


        return {

            "controller": self.name(),

            "port": self.port,

            "running": running,

            "pid": pid,

            "health":
                "OK" if running else "DOWN",

            "uptime_seconds": uptime

        }


    def name(self):

        return "osken"
