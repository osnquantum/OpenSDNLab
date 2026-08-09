import time


class RuntimeState:

    _state = {
        "status": "IDLE",
        "experiment_id": None,
        "stage": None,
        "start_time": None,
        "controller": None,
        "hosts": 0,
        "switches": 0,
        "metrics": {}
    }


    @classmethod
    def update(cls, **kwargs):
        cls._state.update(kwargs)


    @classmethod
    def get(cls):

        data = cls._state.copy()

        if data["start_time"]:
            data["elapsed_seconds"] = round(
                time.time() - data["start_time"],
                2
            )

        return data
