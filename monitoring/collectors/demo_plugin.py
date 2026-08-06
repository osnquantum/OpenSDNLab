from core.plugin import Plugin
from core.interfaces.metric_plugin import IMetricPlugin


PLUGIN = Plugin(

    id="demo",

    name="Demo Collector",

    version="1.0",

    author="OpenSDNLab",

    category="metric",

    description="Framework demonstration plugin",

    supports=[

        "ipv4",

        "ipv6"

    ]

)


class DemoCollector(IMetricPlugin):

    def collect(self, *args, **kwargs):

        print("Collecting demo metric...")


def register(registry):

    registry.register(

        PLUGIN,

        DemoCollector

    )
