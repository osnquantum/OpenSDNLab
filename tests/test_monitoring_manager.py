from monitoring.monitoring_manager import MonitoringManager

manager = MonitoringManager()

print()

print("Monitoring Manager")

print("------------------")

print("Ping Collector      :", type(manager.ping).__name__)
print("Throughput Collector:", type(manager.throughput).__name__)

