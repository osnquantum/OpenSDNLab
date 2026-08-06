from dataclasses import dataclass


@dataclass
class Link:

    source: str

    destination: str

    bandwidth: int = 100

    delay: str = "1ms"

    loss: float = 0.0
