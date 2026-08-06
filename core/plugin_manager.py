"""
OpenSDNLab Plugin Manager

Automatically discovers and registers plugins.
"""

from importlib import import_module
from pathlib import Path

from core.plugin_registry import plugin_registry


class PluginManager:

    def __init__(self):

        self.packages = [
            "controllers",
            "monitoring.collectors"
        ]

    ############################################################

    def discover(self):

        for package in self.packages:

            self.load_package(package)

    ############################################################

    def load_package(self, package):

        package_path = Path(package.replace(".", "/"))

        if not package_path.exists():

            return

        for file in package_path.glob("*.py"):

            if file.stem.startswith("_"):

                continue

            module_name = package + "." + file.stem

            try:

                module = import_module(module_name)

                if hasattr(module, "register"):

                    module.register(plugin_registry)

                    print(f"Loaded {module_name}")

            except Exception as error:

                print(f"Failed {module_name}: {error}")


plugin_manager = PluginManager()
