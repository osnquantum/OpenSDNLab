"""
Plugin Manager
"""

from engine.core.registry import ServiceRegistry


class PluginManager:

    def __init__(self):

        self.registry = ServiceRegistry()

    ############################################################

    def register(self, plugin):

        plugin.initialize()

        self.registry.register(
            plugin.name,
            plugin
        )

    ############################################################

    def get(self, name):

        return self.registry.get(name)

    ############################################################

    def plugins(self):

        return self.registry._services

