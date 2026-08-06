"""
Insight Engine
"""

from analytics.insight import Insight


class InsightEngine:

    ############################################################

    def analyze_delay(self, results):

        if len(results) < 2:

            return None

        first = results[0]

        last = results[-1]

        delta = last["average_rtt"] - first["average_rtt"]

        if delta > 0:

            return Insight(

                title="Delay Analysis",

                observation=(
                    f"Average RTT increased from "
                    f"{first['average_rtt']} ms "
                    f"to {last['average_rtt']} ms."
                ),

                explanation=(
                    "Increasing link delay increased "
                    "end-to-end latency."
                ),

                recommendation=(
                    "Repeat the experiment using "
                    "different bandwidth values."
                )

            )

        return Insight(

            title="Delay Analysis",

            observation="No RTT increase observed.",

            explanation="Delay had little measurable impact.",

            recommendation="Verify topology and parameters."

        )
