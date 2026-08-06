from dataclasses import dataclass


@dataclass
class Host:

    name: str

    ipv4: str = ""

    ipv6: str = ""

    mac: str = ""
