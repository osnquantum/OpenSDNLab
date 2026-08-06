"""
Delay Analysis
"""

from analyses.base_analysis import BaseAnalysis


class DelayAnalysis(BaseAnalysis):

    def generate_configurations(self):

        print("Generating delay configurations...")

        return []

    ############################################################

    def execute(self):

        print("Executing delay experiments...")

    ############################################################

    def compare(self, results):

        print("Comparing delay experiment results...")

    ############################################################

    def report(self, results):

        print("Generating delay report...")
