"""
OpenSDNLab Plugin Registry
"""

from core.plugin import Plugin


class PluginRegistry:

    def __init__(self):

        self._plugins = {}

    ############################################################

    def register(

        self,

        plugin: Plugin,

        implementation

    ):

        self._plugins.setdefault(plugin.category, {})

        self._plugins[plugin.category][plugin.id] = {

            "plugin": plugin,

            "implementation": implementation

        }

    ############################################################

    def get(

        self,

        category,

        plugin_id

    ):

        return self._plugins[category][plugin_id]

    ############################################################

    def list(

        self,

        category=None

    ):

        if category is None:

            return self._plugins

        return self._plugins.get(category, {})


plugin_registry = PluginRegistry()
