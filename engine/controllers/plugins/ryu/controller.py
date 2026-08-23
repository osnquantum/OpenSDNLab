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


    def get_topology(self):
        """
        Return topology information for the Ryu controller.

        Ryu integration is not implemented yet, so return the
        standard OpenSDNLab empty topology representation.
        """

        return {
            "controller": self.name(),
            "switches": [],
            "links": [],
            "switch_count": 0,
            "link_count": 0,
            "available": False
        }
