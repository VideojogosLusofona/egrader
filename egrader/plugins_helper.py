from importlib.metadata import EntryPoints, entry_points
from typing import AbstractSet, Any, Dict, Final

from .common import get_desc

PLUGINS_ASSESS_REPO: Final[str] = "egrader.assess_repo"
PLUGINS_ASSESS_INTER_REPO: Final[str] = "egrader.assess_inter_repo"
PLUGINS_REPORT: Final[str] = "egrader.report"


def list_plugins(args):
    """List available plugins."""

    plugin_types = (
        ("Repository assessment plugins", PLUGINS_ASSESS_REPO),
        ("Inter-repository assessment plugins", PLUGINS_ASSESS_INTER_REPO),
        ("Reporting plugins", PLUGINS_REPORT),
    )

    for plugin_type in plugin_types:

        plugins: EntryPoints = entry_points(group=plugin_type[1])
        print(f"{plugin_type[0]}:")
        for plugin in plugins:
            print(f"\t{plugin.name}\t{get_desc(plugin.load())}")
        print()

class LoadPluginError(Exception):
    """Error raised when a required plugin fails to load."""


def load_plugin_functions(
    plugin_group: str, required: AbstractSet[str]
) -> Dict[str, Any]:
    """Load required plugins from the specified plugin group."""

    # Load plugins
    plugins: EntryPoints = entry_points(group=plugin_group)

    # Set of existing plugin names
    plugin_names: AbstractSet[str] = {plugin.name for plugin in plugins}

    # Are there any required plugins not in the existing plugins set?
    plugins_not_found = required - plugin_names
    if len(plugins_not_found) > 0:
        raise LoadPluginError(f"Required plugins {plugins_not_found} not found.")

    # Load required plugins
    plugin_functions: Dict[str, Any] = {}
    for plugin in plugins:
        if plugin.name in required:
            plugin_functions[plugin.name] = plugin.load()

    return plugin_functions
