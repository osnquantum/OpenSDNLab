"""
Comparison Engine
"""

from analytics.comparison_result import ComparisonResult


class ComparisonEngine:

    def compare(

        self,

        scenario_name,

        experiment_results

    ):

        comparison = ComparisonResult(

            scenario=scenario_name

        )

        comparison.results.extend(

            experiment_results

        )

        return comparison
