from analyses.analysis import Analysis
from analyses.analysis_variable import AnalysisVariable
from analyses.analysis_engine import AnalysisEngine


analysis = Analysis(

    name="QoS Analysis"

)

analysis.variables.append(

    AnalysisVariable(

        "delay",

        [

            "1ms",

            "5ms",

            "10ms"

        ]

    )

)

analysis.variables.append(

    AnalysisVariable(

        "bandwidth",

        [

            "10Mbps",

            "100Mbps"

        ]

    )

)

engine = AnalysisEngine()

configs = engine.generate(

    analysis

)

print()

print("Generated Configurations")

print("------------------------")

for config in configs:

    print(config)
