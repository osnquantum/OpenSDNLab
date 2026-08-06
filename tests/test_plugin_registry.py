from core.plugin_registry import plugin_registry


plugin_registry.register(

    "controller",

    "osken",

    "OSKen Controller"

)

plugin_registry.register(

    "metric",

    "ping",

    "Ping Collector"

)

plugin_registry.register(

    "metric",

    "throughput",

    "Throughput Collector"

)

print()

print(plugin_registry.list())

print()

print(plugin_registry.get(

    "controller",

    "osken"

))

print()

print(plugin_registry.list("metric"))
