from analyses.analysis import Analysis
from analyses.analysis_variable import AnalysisVariable
from analyses.analysis_runner import AnalysisRunner


analysis = Analysis(

    name="Delay Study"

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

runner = AnalysisRunner()

runner.execute(analysis)
