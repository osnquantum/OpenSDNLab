from pathlib import Path


class ControllerLogReader:


    LOG_FILES = {

        "osken":
        "logs/osken.log"

    }


    @classmethod
    def read(cls, controller):

        file = cls.LOG_FILES.get(controller)


        if not file:

            return []


        path = Path(file)


        if not path.exists():

            return []


        lines = path.read_text(
            errors="ignore"
        ).splitlines()


        return lines[-100:]
