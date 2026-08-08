"""
Research Correlation Analysis
"""

import statistics


class CorrelationService:


    def pearson(self, x, y):

        x = [float(v) for v in x]
        y = [float(v) for v in y]


        n = len(x)

        if n < 2:
            return 0


        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)


        numerator = sum(
            (a-mean_x)*(b-mean_y)
            for a,b in zip(x,y)
        )


        denominator = (

            sum(
                (a-mean_x)**2
                for a in x
            )
            *
            sum(
                (b-mean_y)**2
                for b in y
            )

        ) ** 0.5


        if denominator == 0:
            return 0


        return round(
            numerator / denominator,
            4
        )



    def analyze(self, data):


        return {


            "rtt_throughput":

            self.pearson(
                data["rtt"],
                data["throughput"]
            ),



            "rtt_jitter":

            self.pearson(
                data["rtt"],
                data["jitter"]
            ),



            "delay_throughput":

            self.pearson(
                data["one_way_delay"],
                data["throughput"]
            )

        }
