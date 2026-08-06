from repository.experiment_repository import ExperimentRepository
from repository.models import ExperimentResult

repo = ExperimentRepository()

result = ExperimentResult(
    experiment_name="Repository Demo",
    topology="linear",
    controller="osken",
    protocol="ipv4",
    average_rtt=8.28,
    packet_loss=0.0,
    throughput=86.90
)

filename = repo.save(result)

print()
print("Saved:", filename)
