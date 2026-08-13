import time


class ControllerLogger:

    logs = []


    @classmethod
    def add(cls, message):

        cls.logs.append({
            "time": time.strftime("%H:%M:%S"),
            "message": message
        })


        if len(cls.logs) > 200:
            cls.logs = cls.logs[-200:]


    @classmethod
    def get(cls):

        return cls.logs
