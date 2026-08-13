from flask import Blueprint

from server.services.system_service import SystemService


system = Blueprint(
    "system",
    __name__,
)


service = SystemService()



@system.route("/start", methods=["POST"])
def start():

    return service.start()



@system.route("/stop", methods=["POST"])
def stop():

    return service.stop()



@system.route("/restart", methods=["POST"])
def restart():

    return service.restart()



@system.route("/status")
def status():

    return service.status()



@system.route("/readiness")
def readiness():

    return service.readiness()
