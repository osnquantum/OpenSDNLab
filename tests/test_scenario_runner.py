from scenario.scenario_runner import ScenarioRunner


class DummyManager:

    def run(self, configuration):

        print("Executing experiment...")

        return {

            "status":"success",

            "metadata":configuration.metadata

        }


from models.experiment_configuration import ExperimentConfiguration

configs = []

for delay in ["1ms","5ms","10ms"]:

    c = ExperimentConfiguration(

        name="Delay"

    )

    c.metadata["delay"] = delay

    configs.append(c)


runner = ScenarioRunner(

    DummyManager()

)

results = runner.run(

    configs

)

print()

print(results)
