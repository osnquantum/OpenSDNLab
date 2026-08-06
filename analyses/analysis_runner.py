"""
Analysis Runner
"""

from analyses.analysis_engine import AnalysisEngine
from services.experiment_manager import ExperimentManager


class AnalysisRunner:

    def __init__(self):

        self.engine = AnalysisEngine()

        self.manager = ExperimentManager()

    ############################################################

    def execute(self, analysis):

        configurations = self.engine.generate(analysis)

        print()

        print("Generated Configurations")

        print("--------------------------------")

        for configuration in configurations:

            print(configuration)

        # Next Sprint:
        # Convert each configuration into
        # ExperimentConfiguration
        # then call manager.run_batch()

        return configurations
