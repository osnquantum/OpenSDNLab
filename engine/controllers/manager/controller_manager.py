import importlib
from engine.controllers.controller_logger import ControllerLogger
import yaml


CONFIG_FILE = (
    "engine/controllers/config/controllers.yaml"
)


class ControllerManager:


    def __init__(self):

        self.controllers = {}

        self.active_controller = None

        self.load_controllers()



    def load_controllers(self):

        with open(CONFIG_FILE) as f:

            config = yaml.safe_load(f)


        local = config.get(
            "controllers",
            {}
        ).get(
            "local",
            {}
        ).get(
            "available",
            {}
        )


        for name, info in local.items():

            class_path = info.get(
                "class"
            )

            if not class_path:
                continue


            module_name, class_name = class_path.rsplit(
                ".",
                1
            )


            module = importlib.import_module(
                module_name
            )


            controller_class = getattr(
                module,
                class_name
            )


            self.controllers[name] = controller_class()



    def list(self):

        return list(
            self.controllers.keys()
        )



    def start(self, name):

        name = name.lower()


        if self.active_controller:

            if self.active_controller != name:

                ControllerLogger.add(
                    f"Stopping active controller: {self.active_controller}"
                )

                self.stop(
                    self.active_controller
                )


        ControllerLogger.add(
            f"Starting controller: {name}"
        )


        result = self.get(name).start()


        self.active_controller = name


        ControllerLogger.add(
            f"Controller active: {name}"
        )


        return result



    def get(self, name):

        name = name.lower()

        if name not in self.controllers:

            raise Exception(
                f"Unsupported controller: {name}"
            )

        return self.controllers[name]



    def stop(self, name):

        name = name.lower()


        ControllerLogger.add(
            f"Stopping controller: {name}"
        )


        result = self.get(name).stop()


        if self.active_controller == name:

            self.active_controller = None


        ControllerLogger.add(
            f"Controller stopped: {name}"
        )


        return result



    def status(self, name):

        return self.get(name).status()
