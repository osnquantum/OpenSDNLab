from analyses.delay_analysis import DelayAnalysis


analysis = DelayAnalysis()

configs = analysis.generate_configurations()

analysis.execute()

analysis.compare([])

analysis.report([])
