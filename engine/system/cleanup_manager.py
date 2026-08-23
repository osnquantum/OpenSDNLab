"""
OpenSDNLab Global Cleanup Manager
"""

import os
import subprocess

from engine.core.logger import logger


class CleanupManager:


    @staticmethod
    def run_command(cmd):

        try:
            subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        except Exception:
            pass



    @classmethod
    def cleanup(cls):

        logger.info(
            "Starting deep network cleanup"
        )


        commands = [

            # Do not use global `mn -c` here.
            # The Flask API and OS-Ken controller are long-running
            # processes and experiment cleanup must not broadly kill
            # unrelated runtime processes.

            # Remove only stale Mininet interfaces.

            # Remove stale namespaces
            "ip netns list | awk '{print $1}' | xargs -r -n1 ip netns delete",

            # Remove stale interfaces
            "ip link show | grep -o '[a-zA-Z0-9_-]*-eth[0-9]*' | xargs -r -n1 ip link delete",

            # Clear OVS bridges
            "ovs-vsctl list-br | xargs -r -n1 ovs-vsctl del-br",

            # Remove stale qdisc
            "tc qdisc del dev lo root 2>/dev/null || true"

        ]


        for cmd in commands:

            cls.run_command(cmd)


        logger.info(
            "Deep cleanup completed"
        )
