from flask import Blueprint, jsonify

from engine.controllers.manager.controller_manager import ControllerManager
from engine.controllers.log_reader import ControllerLogReader
from engine.controllers.controller_logger import ControllerLogger


controllers_api = Blueprint(
    "controllers_api",
    __name__
)


manager = ControllerManager()



@controllers_api.route(
    "/api/controllers",
    methods=["GET"]
)
def list_controllers():

    result = []

    for name in manager.list():

        result.append({

            "name": name,

            "status":
                manager.status(name)

        })


    return jsonify(result)



@controllers_api.route(
    "/api/controllers/<name>/start",
    methods=["POST"]
)
def start_controller(name):

    return jsonify(
        manager.start(name)
    )



@controllers_api.route(
    "/api/controllers/<name>/stop",
    methods=["POST"]
)
def stop_controller(name):

    return jsonify({

        "success":
            manager.stop(name)

    })



@controllers_api.route(
    "/api/controllers/<name>/restart",
    methods=["POST"]
)
def restart_controller(name):

    manager.stop(name)

    return jsonify(
        manager.start(name)
    )


@controllers_api.route(
    "/api/controllers/logs",
    methods=["GET"]
)
def controller_logs():

    return jsonify(
        ControllerLogger.get()
    )



@controllers_api.route(
    "/api/controllers/<name>/logs",
    methods=["GET"]
)
def controller_file_logs(name):

    return jsonify(
        ControllerLogReader.read(name)
    )



@controllers_api.route(
    "/api/controllers/<name>/live-logs",
    methods=["GET"]
)
def controller_live_logs(name):

    system_logs = ControllerLogger.get()

    controller_logs = ControllerLogReader.read(name)


    merged = []


    for log in system_logs:

        merged.append({

            "source": "SYSTEM",

            "time": log["time"],

            "message": log["message"]

        })


    for line in controller_logs:

        merged.append({

            "source": name.upper(),

            "time": "",

            "message": line

        })


    return jsonify(merged)



@controllers_api.route(
    "/api/controllers/active",
    methods=["GET"]
)
def active_controller():

    return jsonify({

        "active":
            manager.active_controller

    })

