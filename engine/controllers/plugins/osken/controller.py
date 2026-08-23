import subprocess
import os
import signal
import time
import json

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

        # Reuse only the process owned by this controller instance.
        if self.process and self.process.poll() is None:

            ControllerLogger.add(
                f"OSKen already running PID={self.process.pid}"
            )

            return {
                "controller": self.name(),
                "pid": self.process.pid,
                "port": self.port,
                "running": True,
                "reused": True
            }

        # Do not silently reuse an unknown OS-Ken process.
        # A process listening on the OpenFlow port must be cleaned
        # up explicitly before this controller starts.
        port_check = subprocess.run(
            [
                "ss",
                "-ltn",
                f"sport = :{self.port}"
            ],
            capture_output=True,
            text=True
        )

        # Ignore the header line. Any additional line means
        # something is actually listening on this exact port.
        listening_lines = [
            line
            for line in port_check.stdout.splitlines()
            if line.strip()
            and not line.strip().startswith("State")
        ]

        if listening_lines:

            raise RuntimeError(
                f"Port {self.port} is already in use by "
                "another process"
            )

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

            self.process = None

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
            "running": True,
            "reused": False
        }


    def stop(self):

        ControllerLogger.add(
            "Stopping managed OSKen controller"
        )

        if self.process:

            try:

                if self.process.poll() is None:

                    self.process.terminate()

                    self.process.wait(
                        timeout=5
                    )

            except subprocess.TimeoutExpired:

                self.process.kill()

                self.process.wait()

            finally:

                self.process = None

        self.start_time = None

        ControllerLogger.add(
            "Managed OSKen controller stopped"
        )

        return True


    def status(self):

        running = (
            self.process is not None
            and self.process.poll() is None
        )

        pid = (
            self.process.pid
            if running
            else None
        )

        uptime = None

        if running and self.start_time:

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
            "health": (
                "OK"
                if running
                else "DOWN"
            ),
            "uptime_seconds": uptime
        }


    def get_topology(self):
        """
        Return the topology discovered by the running OS-Ken
        controller using the OpenSDNLab standard representation.
        """

        topology_path = os.path.join(
            project_root,
            "runtime",
            "controller_stats",
            "osken_topology.json"
        )

        if not os.path.exists(topology_path):

            return {
                "controller": self.name(),
                "switches": [],
                "links": [],
                "switch_count": 0,
                "link_count": 0,
                "available": False
            }

        try:

            with open(topology_path, "r") as f:

                topology = json.load(f)

        except Exception as error:

            ControllerLogger.add(
                f"Failed to read OS-Ken topology: {error}"
            )

            return {
                "controller": self.name(),
                "switches": [],
                "links": [],
                "switch_count": 0,
                "link_count": 0,
                "available": False,
                "error": str(error)
            }

        topology["controller"] = self.name()

        topology["available"] = True

        return topology


    def name(self):

        return "osken"
