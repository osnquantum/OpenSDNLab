import subprocess
import os
import signal
import time

from engine.controllers.base_controller import BaseController
from engine.controllers.controller_logger import ControllerLogger


project_root = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../.."
    )
)


class OsKenController(BaseController):

    def __init__(self):

        self.process = None
        self.port = 6653
        self.start_time = None


    def start(self):

        ControllerLogger.add(
            "OSKen start requested"
        )

        # If another OS-Ken instance is already listening on
        # the OpenFlow port, reuse it instead of starting a duplicate.
        port_check = subprocess.run(
            [
                "ss",
                "-ltn"
            ],
            capture_output=True,
            text=True
        )

        if f":{self.port}" in port_check.stdout:

            pid_result = subprocess.run(
                [
                    "pgrep",
                    "-o",
                    "-f",
                    "osken-manager"
                ],
                capture_output=True,
                text=True
            )

            existing_pid = pid_result.stdout.strip()

            ControllerLogger.add(
                f"OSKen already running on port "
                f"{self.port}, PID={existing_pid}"
            )

            return {
                "controller": self.name(),
                "pid": existing_pid,
                "port": self.port,
                "running": True,
                "reused": True
            }

        # Ensure only one OS-Ken process exists.
        self.stop()

        ControllerLogger.add(
            "Launching OSKen controller process"
        )

        os.makedirs(
            os.path.join(project_root, "logs"),
            exist_ok=True
        )

        log_path = os.path.join(
            project_root,
            "logs",
            "osken.log"
        )

        log_file = open(
            log_path,
            "w"
        )

        self.process = subprocess.Popen(
            [
                "osken-manager",
                "--observe-links",
                "--ofp-tcp-listen-port",
                str(self.port),
                "engine.controllers.apps.simple_switch_13"
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            cwd=project_root,
            env={
                **os.environ,
                "PYTHONPATH": (
                    project_root
                    + ":"
                    + os.environ.get(
                        "PYTHONPATH",
                        ""
                    )
                )
            }
        )

        self.start_time = time.time()

        time.sleep(2)

        if self.process.poll() is not None:

            raise RuntimeError(
                "OSKen failed to start. "
                "Check logs/osken.log"
            )

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

        ControllerLogger.add(
            "Stopping all OSKen processes"
        )

        # Stop the process owned by this controller object.
        if self.process:

            try:
                self.process.terminate()

                self.process.wait(
                    timeout=5
                )

            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass

        # Kill orphaned OS-Ken processes.
        subprocess.run(
            [
                "pkill",
                "-9",
                "-f",
                "osken-manager"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

        # Wait until port 6653 is actually released.
        for _ in range(10):

            result = subprocess.run(
                [
                    "ss",
                    "-ltn"
                ],
                capture_output=True,
                text=True
            )

            if f":{self.port}" not in result.stdout:

                break

            time.sleep(1)

        else:

            raise RuntimeError(
                f"Port {self.port} is still in use"
            )

        self.process = None
        self.start_time = None

        ControllerLogger.add(
            "OSKen stopped and port released"
        )

        return True


    def status(self):

        result = subprocess.run(
            [
                "pgrep",
                "-o",
                "-f",
                "osken-manager"
            ],
            capture_output=True,
            text=True
        )

        running = result.returncode == 0

        pid = (
            result.stdout.strip()
            if running
            else None
        )

        uptime = None

        if (
            running
            and self.start_time
        ):

            uptime = round(
                time.time()
                - self.start_time,
                2
            )

        return {

            "controller": self.name(),

            "port": self.port,

            "running": running,

            "pid": pid,

            "health":
                "OK"
                if running
                else "DOWN",

            "uptime_seconds": uptime

        }


    def name(self):

        return "osken"
