"""
Dynamic Metric Registry

Provides access to available research metrics
"""

import sqlite3


DB_PATH = "storage/database/opensdnlab.db"


class MetricRegistry:


    def get_metric(self, name):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM metric_registry
            WHERE metric_name=?
            """,
            (name,)
        )

        result = cursor.fetchone()

        conn.close()

        return result



    def get_all_metrics(self):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM metric_registry
            WHERE enabled=1
            """
        )

        result = cursor.fetchall()

        conn.close()

        return result



    def get_by_category(self, category):

        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM metric_registry
            WHERE category=?
            """,
            (category,)
        )

        result = cursor.fetchall()

        conn.close()

        return result
