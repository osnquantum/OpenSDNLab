"""
Analysis Engine
"""

from itertools import product


class AnalysisEngine:

    ############################################################

    def generate(self, analysis):

        variables = analysis.variables

        names = [v.name for v in variables]

        values = [v.values for v in variables]

        combinations = []

        for combo in product(*values):

            combinations.append(

                dict(

                    zip(

                        names,

                        combo

                    )

                )

            )

        return combinations
