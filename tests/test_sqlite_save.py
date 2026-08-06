from repository.sqlite.sqlite_repository import SQLiteRepository
from repository.models import ExperimentResult

repo = SQLiteRepository()

result = ExperimentResult(

    experiment_name="SQLite Demo",

    experiment_id="EXP-0002",

    topology="linear",

    hosts=2,

    switches=1,

    links=2,

    protocol="ipv4",

    controller="osken",

    bandwidth=100,

    delay="1ms",

    loss=0.0,

    minimum_rtt=5.5,

    average_rtt=6.2,

    maximum_rtt=7.1,

    jitter=0.8,

    packet_loss=0.0,

    throughput=125.0

)

row = repo.save(result)

print()

print("Inserted Row ID:", row)
