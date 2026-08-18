"""
Controller Impact Analysis
"""

import statistics


class ControllerAnalysisService:


    def pearson(self, x, y):

        if len(x) < 2:
            return 0

        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)

        numerator = sum(
            (a-mean_x)*(b-mean_y)
            for a,b in zip(x,y)
        )

        denominator = (
            sum((a-mean_x)**2 for a in x)
            *
            sum((b-mean_y)**2 for b in y)
        ) ** 0.5


        if denominator == 0:
            return 0


        return round(
            numerator / denominator,
            4
        )


    def analyze(
        self,
        controller_data,
        qos_data
    ):

        return {

            "packet_in_vs_rtt":
                self.pearson(
                    controller_data["packet_in"],
                    qos_data["rtt"]
                ),


            "flow_install_vs_rtt":
                self.pearson(
                    controller_data["flows"],
                    qos_data["rtt"]
                ),


            "memory_vs_rtt":
                self.pearson(
                    controller_data["memory"],
                    qos_data["rtt"]
                )

        }
