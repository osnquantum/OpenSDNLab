"""
Stable network entity identifiers.

Provides canonical identifiers for datapaths, directional links,
paths, and monitored flows.

These identifiers are used by history, analytics, recovery,
prediction, and adaptive decision components.
"""


class NetworkIdentity:

    @staticmethod
    def datapath_id(dpid):
        """
        Return a canonical datapath identifier.
        """

        return f"dpid:{int(dpid)}"


    @staticmethod
    def directional_link_id(
        src_dpid,
        src_port,
        dst_dpid,
        dst_port,
    ):
        """
        Return a canonical directional link identifier.

        Example:
        dpid:1:port:2->dpid:2:port:1
        """

        return (
            f"{NetworkIdentity.datapath_id(src_dpid)}"
            f":port:{int(src_port)}"
            "->"
            f"{NetworkIdentity.datapath_id(dst_dpid)}"
            f":port:{int(dst_port)}"
        )


    @staticmethod
    def path_id(path):
        """
        Return a canonical path identifier.

        Example:
        [1, 2, 4]

        becomes:

        dpid:1->dpid:2->dpid:4
        """

        return "->".join(
            NetworkIdentity.datapath_id(dpid)
            for dpid in path
        )


    @staticmethod
    def flow_id(
        source,
        destination,
        protocol=None,
    ):
        """
        Return a canonical monitored-flow identifier.

        Example:
        h1->h2:tcp
        """

        identity = (
            f"{source}"
            "->"
            f"{destination}"
        )

        if protocol:
            identity += f":{str(protocol).lower()}"

        return identity


network_identity = NetworkIdentity()
