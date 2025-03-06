# Copyright (C) 2022-2025 Nuno Fachada and contributors
# Licensed under the GNU General Public License v3.0 or later.
# See <https://www.gnu.org/licenses/gpl-3.0.html> for details.

"""Plug-in handling functionality."""

from enum import Enum
from importlib.metadata import EntryPoints, entry_points
from inspect import getdoc
from typing import AbstractSet, Any, Dict


class PluginLoadError(Exception):
    """Error raised when a required plugin fails to load."""


class PluginTypes(Enum):
    """Plugin types and functionality."""

    Loader = ("egrader.loader", "Rules loader plugins")
    Repo = ("egrader.assess_repo", "Repository assessment plugins")
    InterRepo = ("egrader.assess_inter_repo", "Inter-repository assessment plugins")
    Report = ("egrader.report", "Reporting plugins")

    def __init__(self, group, description):
        """Initialize plugin types enum."""
        self.group = group
        self.description = description

    def load_functions(self, required: AbstractSet[str]) -> Dict[str, Any]:
        """Load all plugin functions of this type."""
        # Load plugins
        plugins: EntryPoints = entry_points(group=self.group)

        # Set of existing plugin names
        plugin_names: AbstractSet[str] = {plugin.name for plugin in plugins}

        # Are there any required plugins not in the existing plugins set?
        plugins_not_found: AbstractSet[str] = required - plugin_names
        if len(plugins_not_found) > 0:
            raise PluginLoadError(f"Required plugins {plugins_not_found} not found.")

        # Load all plugins
        plugin_functions: Dict[str, Any] = {}
        for plugin in plugins:
            plugin_functions[plugin.name] = plugin.load()

        return plugin_functions

    def load_function(self, plugin_name: str) -> Any:
        """Load a specific plugin function."""
        # Obtain the specified plugin entry point
        plugins: EntryPoints = entry_points(group=self.group, name=plugin_name)

        # If plugin not found, raise error
        if plugin_name not in plugins.names:
            raise PluginLoadError(
                f"Plugin {plugin_name!r} not found in {self.group!r} group"  # noqa: E713
            )

        # Otherwise, return plugin function
        return plugins[plugin_name].load()

    @staticmethod
    def short_description(func) -> str:
        """Get a short description of a plugin."""
        desc: str | None = getdoc(func)

        if desc is not None and len(desc) > 0:
            desc = desc.split("\n")[0]
        else:
            desc = "Unavailable"

        return desc

    @staticmethod
    def print_all():
        """Print all available plugins."""
        for plugin_type in PluginTypes:
            plugins: EntryPoints = entry_points(group=plugin_type.group)
            print(f":: {plugin_type.description}\n")
            for plugin in plugins:
                print(f"\t{plugin.name}\n\t\t{PluginTypes.short_description(plugin.load())}")
            print()
