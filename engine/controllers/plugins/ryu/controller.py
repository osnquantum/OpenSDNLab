from engine.controllers.base_controller import BaseController


class RyuController(BaseController):


    def start(self):

        return {

            "controller": self.name(),

            "status": "not implemented"

        }


    def stop(self):

        return True


    def status(self):

        return {

            "controller": self.name()

        }


    def name(self):

        return "ryu"
