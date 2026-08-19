from dataclasses import dataclass


@dataclass
class Link:

    source: str

    destination: str

    bandwidth: int = 100

    delay: str = "1ms"

    loss: float = 0.0

    # Optional explicit interface/port numbers.
    # None keeps Mininet's automatic port allocation.
    source_port: int | None = None

    destination_port: int | None = None
