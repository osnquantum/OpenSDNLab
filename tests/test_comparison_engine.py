from analytics.comparison_engine import ComparisonEngine
from analytics.statistics_engine import StatisticsEngine


results = [

    {

        "delay":"1ms",

        "average_rtt":6.2,

        "throughput":138

    },

    {

        "delay":"5ms",

        "average_rtt":10.4,

        "throughput":129

    },

    {

        "delay":"10ms",

        "average_rtt":17.6,

        "throughput":118

    }

]


comparison = ComparisonEngine()

report = comparison.compare(

    "Delay Study",

    results

)

stats = StatisticsEngine()

print()

print(report.scenario)

print()

print(report.results)

print()

print(

    "Average RTT:",

    stats.average(

        [

            r["average_rtt"]

            for r in results

        ]

    )

)

print(

    "Average Throughput:",

    stats.average(

        [

            r["throughput"]

            for r in results

        ]

    )

)
