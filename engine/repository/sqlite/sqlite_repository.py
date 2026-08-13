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

            one_way_delay REAL,

                created_at TEXT,

                status TEXT,

                notes TEXT

            )
            """
        )

        

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS batch_jobs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id TEXT UNIQUE,

                experiment_id TEXT,

                total_runs INTEGER,

                current_run INTEGER DEFAULT 0,

                successful INTEGER DEFAULT 0,

                failed INTEGER DEFAULT 0,

                status TEXT,

                created_at REAL,

                started_at REAL
            )
            '''
        )



        self.connection.commit()


        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS experiment_runs (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                experiment_id TEXT,

                run_number INTEGER,

                minimum_rtt REAL,

                average_rtt REAL,

                maximum_rtt REAL,

                jitter REAL,

                packet_loss REAL,

                throughput REAL,

                estimated_one_way_delay REAL,

                created_at TEXT

            )
            '''
        )

        

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS batch_jobs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id TEXT UNIQUE,

                experiment_id TEXT,

                total_runs INTEGER,

                current_run INTEGER DEFAULT 0,

                successful INTEGER DEFAULT 0,

                failed INTEGER DEFAULT 0,

                status TEXT,

                created_at REAL,

                started_at REAL
            )
            '''
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

            one_way_delay,
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

            :one_way_delay,
                :created_at,
                :status,
                :notes

            )
            """,
            data
        )

        

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS batch_jobs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id TEXT UNIQUE,

                experiment_id TEXT,

                total_runs INTEGER,

                current_run INTEGER DEFAULT 0,

                successful INTEGER DEFAULT 0,

                failed INTEGER DEFAULT 0,

                status TEXT,

                created_at REAL,

                started_at REAL
            )
            '''
        )



        self.connection.commit()

        return cursor.lastrowid



    ############################################################
    # Save repeated experiment measurement run
    ############################################################

    def save_run(
        self,
        experiment_id,
        run_number,
        metrics
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO experiment_runs (

                experiment_id,
                run_number,
                minimum_rtt,
                average_rtt,
                maximum_rtt,
                jitter,
                packet_loss,
                throughput,
                estimated_one_way_delay,
                  mos,
                created_at

            )

            VALUES (

                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                ?,
                datetime('now')

            )
            """,

            (

                experiment_id,
                run_number,

                metrics["minimum_rtt"],
                metrics["average_rtt"],
                metrics["maximum_rtt"],

                metrics["jitter"],
                metrics["packet_loss"],

                metrics["throughput"],

                  metrics["one_way_delay"],

                  metrics["mos"]

            )

        )

        

        self.connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS batch_jobs
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                job_id TEXT UNIQUE,

                experiment_id TEXT,

                total_runs INTEGER,

                current_run INTEGER DEFAULT 0,

                successful INTEGER DEFAULT 0,

                failed INTEGER DEFAULT 0,

                status TEXT,

                created_at REAL,

                started_at REAL
            )
            '''
        )



        self.connection.commit()

        return cursor.lastrowid
