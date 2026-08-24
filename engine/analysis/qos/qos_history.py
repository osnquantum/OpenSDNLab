"""
In-memory history for raw QoS observations.

Stores time-series observations without applying thresholds,
normalization, weights, or QoS classifications.
"""

from collections import defaultdict, deque


class QoSHistory:

    def __init__(self, max_history=None):

        self.max_history = max_history

        self._observations = defaultdict(
            lambda: deque(maxlen=self.max_history)
        )

    def add(self, observation):

        self._observations[
            observation.flow_id
        ].append(
            observation
        )

    def get_flow_history(self, flow_id):

        return list(
            self._observations.get(
                flow_id,
                []
            )
        )

    def get_all_history(self):

        return {
            flow_id: list(observations)
            for flow_id, observations
            in self._observations.items()
        }

    def flow_ids(self):

        return list(
            self._observations.keys()
        )

    def clear_flow(self, flow_id):

        self._observations.pop(
            flow_id,
            None
        )

    def clear(self):

        self._observations.clear()
