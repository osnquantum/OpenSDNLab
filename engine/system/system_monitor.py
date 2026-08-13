import subprocess
import socket


class SystemMonitor:


    def command(self, cmd):

        try:
            return subprocess.getoutput(cmd)
        except Exception as e:
            return str(e)



    def port_check(self, host, port):

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(1)

        try:
            result = sock.connect_ex(
                (host, port)
            )

            sock.close()

            return result == 0

        except:

            return False



    def flask_status(self):

        result = self.command(
            "pgrep -af 'server.app'"
        )

        return {

            "running": bool(result),
            "process": result

        }



    def controller_status(self):

        port = self.port_check(
            "127.0.0.1",
            6653
        )


        return {

            "running": port,

            "port":6653

        }



    def ovs_status(self):

        bridges = self.command(
            "sudo -n ovs-vsctl list-br"
        )


        bridge_list = [
            x for x in bridges.splitlines()
            if x.strip()
        ]


        return {

            "running":
                len(bridge_list) > 0,

            "bridges":
                bridge_list

        }



    def mininet_status(self):

        bridges = self.command(
            "sudo -n ovs-vsctl list-br"
        )


        hosts = self.command(
            "ip link | grep -E 'h[0-9]+-eth'"
        )


        running = bool(
            bridges.strip()
            or
            hosts.strip()
        )


        return {

            "running": running,

            "detected_by":
                "OVS topology"

        }



    def get_status(self):

        return {

            "flask":
                self.flask_status(),

            "controller":
                self.controller_status(),

            "ovs":
                self.ovs_status(),

            "mininet":
                self.mininet_status()

        }
