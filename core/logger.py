"""
OpenSDNLab Logger Module

Provides centralized logging for the entire platform.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler


class Logger:
    """Singleton logger for OpenSDNLab."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        self._initialized = True

        # Create log directory
        log_dir = Path("logs/application")
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / "app.log"

        self.logger = logging.getLogger("OpenSDNLab")
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if self.logger.handlers:
            return

        # Console Handler
        console_handler = RichHandler(
            show_time=True,
            show_level=True,
            show_path=False,
            rich_tracebacks=True
        )

        # File Handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5
        )

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)


logger = Logger()
