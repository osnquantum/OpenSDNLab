"""
OpenSDNLab Controller Runtime Manager
"""

import subprocess
import os
import signal
import time

from engine.core.logger import logger


class ControllerRuntimeManager:

    def __init__(self):

        self.process = None
        self.controller_name = None


    def start(self, controller_name="osken"):

        self.stop()

        self.controller_name = controller_name


        if controller_name == "osken":

            command = [
                "osken-manager",
                "--ofp-tcp-listen-port",
                "6653",
                "engine.controllers.apps.simple_switch_13"
            ]

        else:

            raise ValueError(
                f"Unsupported controller: {controller_name}"
            )


        logger.info(
            f"Starting controller: {controller_name}"
        )


        os.makedirs(
            "logs",
            exist_ok=True
        )

        env = os.environ.copy()

        env["PYTHONPATH"] = os.getcwd()


        self.process = subprocess.Popen(
            command,
            env=env,
            stdout=open(
                "logs/controller.log",
                "w"
            ),
            stderr=subprocess.STDOUT
        )


        time.sleep(3)


        return {
            "controller": controller_name,
            "pid": self.process.pid
        }


    def stop(self):

        logger.info(
            "Stopping existing controller processes"
        )


        if self.process:

            try:
                os.kill(
                    self.process.pid,
                    signal.SIGTERM
                )

            except Exception:
                pass

            self.process = None


        subprocess.run(
            [
                "pkill",
                "-f",
                "osken-manager"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )


        time.sleep(2)

        return True


    def status(self):

        return {
            "controller": self.controller_name,
            "running": self.process is not None
        }
