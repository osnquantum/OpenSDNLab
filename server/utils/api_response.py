from flask import jsonify


def success(data=None, message="Success"):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    })


def error(message="Error", status_code=400):
    response = jsonify({
        "success": False,
        "message": message,
        "data": None
    })
    response.status_code = status_code
    return response
