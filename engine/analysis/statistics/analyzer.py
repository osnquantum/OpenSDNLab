"""
OpenSDNLab Statistical Analyzer

Research-oriented experiment analysis.

Provides:
- Mean
- Median
- Standard deviation
- Percentiles
- IQR based outlier detection
"""

import statistics


class StatisticsAnalyzer:


    ############################################################
    # Percentile calculation
    ############################################################

    def percentile(self, values, p):

        if not values:
            return 0

        values = sorted(values)

        index = int(
            (p / 100) * (len(values) - 1)
        )

        return values[index]


    ############################################################
    # IQR Outlier Detection
    ############################################################

    def detect_outliers(
        self,
        runs,
        metric="average_rtt"
    ):

        values = [
            r[metric]
            for r in runs
        ]


        if len(values) < 4:
            return []


        values_sorted = sorted(values)


        q1 = self.percentile(
            values_sorted,
            25
        )

        q3 = self.percentile(
            values_sorted,
            75
        )


        iqr = q3 - q1


        lower = q1 - (1.5 * iqr)

        upper = q3 + (1.5 * iqr)


        outliers = []


        for index, run in enumerate(runs, start=1):

            value = run[metric]


            if value < lower or value > upper:

                outliers.append({

                    "run_number": index,

                    "metric": metric,

                    "value": value,

                    "lower_limit": lower,

                    "upper_limit": upper

                })


        return outliers



    ############################################################
    # Main analysis
    ############################################################

    def analyze(self, runs):


        if not runs:

            return {}



        rtt = [
            r["average_rtt"]
            for r in runs
        ]


        jitter = [
            r["jitter"]
            for r in runs
        ]


        throughput = [
            r["throughput"]
            for r in runs
        ]


        packet_loss = [
            r["packet_loss"]
            for r in runs
        ]


        delay = [
            r["one_way_delay"]
            for r in runs
        ]



        return {


            "samples":

            len(runs),



            "outliers": {

                "rtt":

                self.detect_outliers(
                    runs,
                    "average_rtt"
                )

            },



            "rtt": {

                "mean":
                statistics.mean(rtt),

                "median":
                statistics.median(rtt),

                "p90":
                self.percentile(rtt,90),

                "p95":
                self.percentile(rtt,95),

                "p99":
                self.percentile(rtt,99),

                "std":
                statistics.stdev(rtt)
                if len(rtt)>1 else 0,

                "min":
                min(rtt),

                "max":
                max(rtt)

            },



            "jitter": {

                "mean":
                statistics.mean(jitter),

                "std":
                statistics.stdev(jitter)
                if len(jitter)>1 else 0

            },



            "throughput": {

                "mean":
                statistics.mean(throughput),

                "p95":
                self.percentile(
                    throughput,
                    95
                ),

                "min":
                min(throughput),

                "max":
                max(throughput)

            },



            "packet_loss": {

                "mean":
                statistics.mean(packet_loss)

            },



            "one_way_delay": {

                "mean":
                statistics.mean(delay),

                "p95":
                self.percentile(
                    delay,
                    95
                ),

                "std":
                statistics.stdev(delay)
                if len(delay)>1 else 0

            }

        }
