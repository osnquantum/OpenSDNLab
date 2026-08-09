import math
import statistics


class StatisticsEngine:


    def mean(self, values):
        return statistics.mean(values)


    def median(self, values):
        return statistics.median(values)


    def minimum(self, values):
        return min(values)


    def maximum(self, values):
        return max(values)


    def std_deviation(self, values):
        return statistics.stdev(values)


    def variance(self, values):
        return statistics.variance(values)


    def percentile(self, values, p):

        values = sorted(values)

        index = (len(values)-1) * p

        lower = math.floor(index)
        upper = math.ceil(index)

        if lower == upper:
            return values[int(index)]

        return (
            values[lower] * (upper-index)
            +
            values[upper] * (index-lower)
        )


    def confidence_interval_95(self, values):

        mean = statistics.mean(values)

        std = statistics.stdev(values)

        margin = 1.96 * (
            std / math.sqrt(len(values))
        )

        return (
            mean-margin,
            mean+margin
        )


    def analyze(self, values):

        return {

            "count": len(values),

            "mean": self.mean(values),

            "median": self.median(values),

            "minimum": self.minimum(values),

            "maximum": self.maximum(values),

            "std_deviation": self.std_deviation(values),

            "variance": self.variance(values),

            "p50": self.percentile(values,0.50),

            "p90": self.percentile(values,0.90),

            "p95": self.percentile(values,0.95),

            "p99": self.percentile(values,0.99),

            "confidence_interval_95":
                self.confidence_interval_95(values)

        }
