"""
Dynamic Metric Collector

Central interface for recording experiment metrics
"""

from engine.metrics.metric_registry import MetricRegistry
from engine.metrics.metric_repository import MetricRepository


class MetricCollector:


    def __init__(self):

        self.registry = MetricRegistry()

        self.repository = MetricRepository()



    def record(
        self,
        experiment_id,
        metric_name,
        value,
        node=None,
        interface=None,
        direction=None,
        metadata=None
    ):

        metric = self.registry.get_metric(
            metric_name
        )


        if metric is None:

            raise ValueError(
                f"Unknown metric: {metric_name}"
            )


        metric_id = metric[0]


        self.repository.save_metric(
            experiment_id=experiment_id,
            metric_id=metric_id,
            value=value,
            node=node,
            interface=interface,
            direction=direction,
            metadata=metadata
        )


        return {

            "metric": metric_name,

            "value": value,

            "unit": metric[3]

        }
