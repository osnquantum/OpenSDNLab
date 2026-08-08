"""
OpenSDNLab Process Manager

Controls background services:
- Flask API
- OS-Ken Controller
"""

import subprocess
import os
import signal


class ProcessManager:


    def stop_process(self, keyword):

        try:

            result = subprocess.check_output(
                ["pgrep", "-f", keyword]
            )

            pids = result.decode().split()

            for pid in pids:

                if int(pid) != os.getpid():

                    os.kill(
                        int(pid),
                        signal.SIGTERM
                    )

            return True


        except subprocess.CalledProcessError:

            return True



    def ensure_single_instance(self, keyword):

        self.stop_process(keyword)

        return True
