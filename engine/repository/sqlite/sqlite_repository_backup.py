"""
SQLite Experiment Repository
"""

import sqlite3
from dataclasses import asdict
from pathlib import Path


class SQLiteRepository:

    def __init__(self):

        db_dir = Path("storage/database")
        db_dir.mkdir(parents=True, exist_ok=True)

        self.database = db_dir / "opensdnlab.db"

        self.connection = sqlite3.connect(self.database, check_same_thread=False)

        self.create_table()

    ############################################################

    def create_table(self):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS experiments (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                experiment_name TEXT,

                experiment_id TEXT,

                topology TEXT,

                hosts INTEGER,

                switches INTEGER,

                links INTEGER,

                protocol TEXT,

                controller TEXT,

                bandwidth REAL,

                delay TEXT,

                loss REAL,

                minimum_rtt REAL,

                average_rtt REAL,

                maximum_rtt REAL,

                jitter REAL,

                packet_loss REAL,

                throughput REAL,

                created_at TEXT,

                status TEXT,

                notes TEXT

            )
            """
        )

        self.connection.commit()

    ############################################################

    def save(self, result):

        data = asdict(result)

        data["created_at"] = str(result.created_at)

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO experiments (

                experiment_name,
                experiment_id,
                topology,
                hosts,
                switches,
                links,
                protocol,
                controller,
                bandwidth,
                delay,
                loss,
                minimum_rtt,
                average_rtt,
                maximum_rtt,
                jitter,
                packet_loss,
                throughput,
                created_at,
                status,
                notes

            )

            VALUES (

                :experiment_name,
                :experiment_id,
                :topology,
                :hosts,
                :switches,
                :links,
                :protocol,
                :controller,
                :bandwidth,
                :delay,
                :loss,
                :minimum_rtt,
                :average_rtt,
                :maximum_rtt,
                :jitter,
                :packet_loss,
                :throughput,
                :created_at,
                :status,
                :notes

            )
            """,
            data
        )

        self.connection.commit()

        return cursor.lastrowid

