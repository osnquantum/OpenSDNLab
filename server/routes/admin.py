from engine.core.logger import logger

from flask import Blueprint, render_template, jsonify
import subprocess

admin = Blueprint(
    "admin",
    __name__
)


def run_cmd(cmd):

    try:
        result=subprocess.getoutput(cmd)
        return result
    except Exception as e:
        return str(e)


@admin.route("/admin")
def page():

    return render_template(
        "admin.html"
    )


@admin.route("/api/admin/status")
def status():

    return jsonify({

        "flask":
            run_cmd(
            "pgrep -af 'server.app'"
            ),

        "ovs":
            run_cmd(
            "ovs-vsctl show"
            ),

        "readiness":
            run_cmd(
            "curl -s http://localhost:8000/api/readiness"
            )

    })


@admin.route("/api/admin/restart", methods=["POST"])
def restart():

    logger.info(
        "ADMIN: Flask restart requested from web panel"
    )

    run_cmd(
        "cd ~/OpenSDNLab && nohup ./admin/restart.sh >/tmp/opensdn_restart.log 2>&1 &"
    )

    logger.info(
        "ADMIN: Flask restart command executed"
    )

    return jsonify({

        "output":
        "Restart command sent. Check service status."

    })


@admin.route("/api/admin/ovs")
def ovs():

    return jsonify({

        "output":
        run_cmd(
        "ovs-vsctl show"
        )

    })


@admin.route("/api/admin/run/<command>")
def run_admin_command(command):

    allowed = {

        "status":
        "./admin/status.sh",

        "ovs":
        "./admin/ovs_check.sh",

        "readiness":
        "./admin/readiness.sh"

    }


    if command not in allowed:

        return jsonify({
            "output":"Command not allowed"
        })


    return jsonify({

        "output":
        run_cmd(
            "cd ~/OpenSDNLab && "
            + allowed[command]
        )

    })



@admin.route("/api/admin/ovs/restart", methods=["POST"])
def ovs_restart():

    return jsonify({

        "output":
        run_cmd(
        "sudo systemctl restart openvswitch-switch"
        )

    })



@admin.route("/api/admin/mininet")
def mininet_status():

    return jsonify({

        "output":
        run_cmd(
        "echo '=== Mininet Interfaces ==='; ip link | grep -E 'h[0-9]+-eth|s[0-9]+-eth'; echo; echo '=== OVS Bridges ==='; sudo ovs-vsctl list-br"
        )

    })

