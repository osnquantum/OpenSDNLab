"""
OpenSDNLab Database Connection

Provides centralized SQLite connection using SQLAlchemy.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.configuration import config
from core.logger import logger


class DatabaseConnection:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        self._initialized = True

        db_path = Path(config.get("database.path"))

        db_path.parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(
            f"sqlite:///{db_path}",
            echo=False
        )

        self.Session = sessionmaker(bind=self.engine)

        logger.info(f"Database connected: {db_path}")

    ##################################################################

    def get_session(self):

        return self.Session()


db = DatabaseConnection()
from database.models import Base
Base.metadata.create_all(db.engine)
