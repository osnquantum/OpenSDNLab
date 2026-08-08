"""
OpenSDNLab Controller Health Check
"""

import socket

from engine.core.logger import logger


class ControllerGuard:


    def is_available(
        self,
        host="127.0.0.1",
        port=6653
    ):

        try:

            sock = socket.socket()

            sock.settimeout(2)

            sock.connect(
                (host, port)
            )

            sock.close()

            return True


        except Exception:

            return False



    def check(self):

        if self.is_available():

            logger.info(
                "SDN Controller available"
            )

            return True


        logger.warning(
            "SDN Controller unavailable"
        )

        return False
