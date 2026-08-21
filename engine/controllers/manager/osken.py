import subprocess
import os
import signal

project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../.."
    )
)


class OsKenController:

    def __init__(self):

        self.process = None
        self.port = 6653


    def start(self):

        self.stop()

        self.process = subprocess.Popen(
            [
                "osken-manager",
                "--observe-links",
                "--ofp-tcp-listen-port",
                "6653",
                "engine.controllers.apps.simple_switch_13"
            ],
            stdout=open(
                "logs/osken.log",
                "w"
            ),
            stderr=subprocess.STDOUT,
            cwd=project_root,
            env={
                **os.environ,
                "PYTHONPATH": (
                    project_root
                    + ":"
                    + os.environ.get("PYTHONPATH", "")
                )
            }
        )

        return {
            "controller": "osken",
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
            "controller": "osken",
            "port": self.port
        }
