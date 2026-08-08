import subprocess
import os
import signal

from engine.controllers.base_controller import BaseController


class OsKenController(BaseController):


    def __init__(self):

        self.process = None
        self.port = 6653


    def start(self):

        self.stop()

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

        return {

            "controller": self.name(),

            "pid": self.process.pid,

            "port": self.port
        }


    def stop(self):

        if self.process:

            os.kill(
                self.process.pid,
                signal.SIGTERM
            )

            self.process = None

        return True


    def status(self):

        return {

            "controller": self.name(),

            "port": self.port
        }


    def name(self):

        return "osken"
