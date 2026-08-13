import time


class RuntimeLogger:

    _logs = []


    @classmethod
    def add(cls, message):

        cls._logs.append({
            "time": time.strftime("%H:%M:%S"),
            "message": message
        })


        if len(cls._logs) > 200:
            cls._logs = cls._logs[-200:]


    @classmethod
    def get(cls):

        return cls._logs
