from analytics.insight_engine import InsightEngine


results = [

    {

        "delay":"1ms",

        "average_rtt":6.4

    },

    {

        "delay":"5ms",

        "average_rtt":9.8

    },

    {

        "delay":"10ms",

        "average_rtt":16.2

    }

]


engine = InsightEngine()

insight = engine.analyze_delay(results)

print()

print(insight.title)

print()

print(insight.observation)

print()

print(insight.explanation)

print()

print(insight.recommendation)
