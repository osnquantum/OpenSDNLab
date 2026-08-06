"""
Statistics Engine
"""

from statistics import mean


class StatisticsEngine:

    def average(

        self,

        values

    ):

        if not values:

            return 0

        return mean(values)
