"""
Delay Analysis Runner
"""

from engine.models.experiment_configuration import ExperimentConfiguration

from engine.analysis.export.csv_exporter import CSVExporter
from engine.analysis.graphs.graph_generator import GraphGenerator

from engine.scenario.scenario import Scenario
from engine.scenario.scenario_variable import ScenarioVariable
from engine.scenario.scenario_engine import ScenarioEngine
from engine.scenario.experiment_generator import ExperimentGenerator

from engine.services.experiment_manager import ExperimentManager


def main():

    print()
    print("=" * 60)
    print("OpenSDNLab - Delay Analysis")
    print("=" * 60)

    ############################################################
    # Base Configuration
    ############################################################

    base = ExperimentConfiguration(name="Delay Analysis")

    ############################################################
    # Scenario
    ############################################################

    scenario = Scenario(name="Delay Study")

    scenario.variables.append(
        ScenarioVariable(
            "delay",
            [
                "1ms",
                "5ms",
                "10ms",
                "20ms",
                "50ms",
            ],
        )
    )

    ############################################################
    # Generate Experiment Configurations
    ############################################################

    engine = ScenarioEngine()

    experiments = engine.generate(scenario)

    generator = ExperimentGenerator()

    configs = generator.generate(base, experiments)

    print()
    print(f"Generated {len(configs)} experiment(s)")
    print()

    ############################################################
    # Execute Experiments
    ############################################################

    manager = ExperimentManager()

    results = manager.run_batch(configs)

    ############################################################
    # Export CSV
    ############################################################

    exporter = CSVExporter()

    try:

        csv_file = exporter.export(results)

        print(f"CSV exported to: {csv_file}")

    except Exception as error:

        print(f"CSV Export Error: {error}")

        raise

    ############################################################
    # Generate Graphs
    ############################################################

    graph_generator = GraphGenerator()

    try:

        graph_generator.generate(csv_file)

        print("Graphs generated successfully.")

    except Exception as error:

        print(f"Graph Generation Error: {error}")

        raise

    ############################################################
    # Summary
    ############################################################

    print()
    print("=" * 60)
    print("Delay Analysis Completed")
    print("=" * 60)
    print()

    print(f"Successful Experiments : {len(results)}")
    print(f"CSV File : {csv_file}")
    print("Graphs saved to results/")


if __name__ == "__main__":

    main()
