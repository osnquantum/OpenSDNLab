from scenarios.delay.increasing_delay import create

from scenario.scenario_engine import ScenarioEngine


scenario = create()

engine = ScenarioEngine()

experiments = engine.generate(

    scenario

)

print()

print(scenario.name)

print()

for experiment in experiments:

    print(experiment)
