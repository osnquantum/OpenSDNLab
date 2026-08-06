from core.plugin_manager import plugin_manager
from core.plugin_registry import plugin_registry

plugin_manager.discover()

print()

plugins = plugin_registry.list()

for category, items in plugins.items():

    print(category)

    print("----------------")

    for plugin_id, data in items.items():

        plugin = data["plugin"]

        print(plugin.id)

        print(plugin.name)

        print(plugin.version)

        print(plugin.author)

        print(plugin.supports)

        print()
