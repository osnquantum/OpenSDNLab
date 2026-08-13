from engine.controllers.plugins.osken.controller import OsKenController
from engine.controllers.plugins.ryu.controller import RyuController



class ControllerManager:


    def __init__(self):

        self.controllers = {

            "osken": OsKenController(),

            "ryu": RyuController()

        }



    def start(self, name):

        name = name.lower()

        if name not in self.controllers:

            raise Exception(
                f"Unsupported controller: {name}"
            )


        return self.controllers[name].start()





    def get(self, name):

        name = name.lower()

        if name not in self.controllers:

            raise Exception(
                f"Unsupported controller: {name}"
            )

        return self.controllers[name]

    def stop(self, name):

        return self.controllers[name.lower()].stop()



    def status(self, name):

        return self.controllers[name.lower()].status()
