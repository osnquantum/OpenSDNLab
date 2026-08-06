from dataset.dataset_builder import DatasetBuilder


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

        "average_rtt":17.8,

        "throughput":118

    }

]


builder = DatasetBuilder()

dataset = builder.build(

    results,

    name="Delay Study"

)

print()

print("Dataset")

print("----------------")

print(dataset.name)

print(dataset.metadata)

print()

for row in dataset.rows:

    print(row)
