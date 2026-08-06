"""
OpenSDNLab Configuration Manager

Loads and manages application configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from core.logger import logger


class Configuration:

    def __init__(self):

        self.config_path = Path("config/settings.yaml")

        self.data = {}

        self.load()

    ####################################################################

    def load(self):

        """Load configuration from YAML."""

        if not self.config_path.exists():

            logger.error(f"Configuration file not found: {self.config_path}")

            return

        with open(self.config_path, "r") as file:

            self.data = yaml.safe_load(file)

        logger.info("Configuration loaded.")

    ####################################################################

    def save(self):

        """Save configuration to YAML."""

        with open(self.config_path, "w") as file:

            yaml.safe_dump(self.data, file, sort_keys=False)

        logger.info("Configuration saved.")

    ####################################################################

    def reload(self):

        """Reload configuration."""

        self.load()

    ####################################################################

    def get(self, key: str, default: Any = None):

        """
        Retrieve nested configuration.

        Example:
            config.get("database.path")
        """

        value = self.data

        for part in key.split("."):

            if isinstance(value, dict):

                value = value.get(part)

            else:

                return default

        return value if value is not None else default

    ####################################################################

    def set(self, key: str, value: Any):

        """
        Update nested configuration.

        Example:
            config.set("database.path","database/test.db")
        """

        keys = key.split(".")

        current = self.data

        for part in keys[:-1]:

            current = current.setdefault(part, {})

        current[keys[-1]] = value

        logger.info(f"Configuration updated: {key} = {value}")

    ####################################################################

    def show(self):

        """Print loaded configuration."""

        print(yaml.dump(self.data, sort_keys=False))


config = Configuration()
