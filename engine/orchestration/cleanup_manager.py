"""
OpenSDNLab Cleanup Manager

Safe cleanup of stale Mininet resources.
"""

import subprocess

from engine.core.logger import logger


class CleanupManager:


    def cleanup_mininet(self):

        logger.info(
            "Checking Mininet cleanup"
        )

        try:

            result = subprocess.run(
                ["mn", "-c"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5
            )

            if result.returncode == 0:

                logger.info(
                    "Mininet cleanup completed"
                )

                return True


            logger.warning(
                "Mininet cleanup returned non-zero"
            )

            return False


        except subprocess.TimeoutExpired:

            logger.warning(
                "Mininet cleanup timeout - continuing"
            )

            return True


        except Exception as error:

            logger.error(
                f"Cleanup error: {error}"
            )

            return False
