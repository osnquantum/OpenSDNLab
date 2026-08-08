"""
Dynamic Metric Repository

Stores experiment metric measurements
"""

import sqlite3
import time


DB_PATH = "storage/database/opensdnlab.db"


class MetricRepository:


    def save_metric(
        self,
        experiment_id,
        metric_id,
        value,
        node=None,
        interface=None,
        direction=None,
        metadata=None
    ):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO metric_values
            (
                experiment_id,
                metric_id,
                timestamp,
                value,
                node,
                interface,
                direction,
                metadata
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                experiment_id,
                metric_id,
                time.time(),
                value,
                node,
                interface,
                direction,
                metadata
            )
        )

        conn.commit()
        conn.close()



    def get_metrics(self, experiment_id):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                metric_values.*,
                metric_registry.metric_name,
                metric_registry.unit

            FROM metric_values

            JOIN metric_registry

            ON metric_values.metric_id =
               metric_registry.id

            WHERE experiment_id=?
            """,
            (experiment_id,)
        )

        result = cursor.fetchall()

        conn.close()

        return result
