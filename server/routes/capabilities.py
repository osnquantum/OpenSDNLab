from flask import Blueprint

from server.utils.api_response import success
from server.services.engine_service import EngineService

capabilities = Blueprint("capabilities", __name__)

engine = EngineService()


@capabilities.route("/capabilities", methods=["GET"])
def get_capabilities():

    return success(
        engine.capabilities(),
        "Capabilities loaded successfully."
    )

