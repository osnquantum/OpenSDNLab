from services.experiment_pipeline import ExperimentPipeline

from experiment.configuration import ExperimentConfiguration

config = ExperimentConfiguration(

    name="Pipeline Demo",

    topology={
        "type": "linear",
        "hosts": 2,
        "switches": 1
    },

    network={
        "protocol": "ipv4"
    },

    controller={
        "type": "local"
    }

)

pipeline = ExperimentPipeline()

pipeline.run(config)

print()

print("Pipeline executed successfully.")

