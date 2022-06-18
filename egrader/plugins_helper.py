from argparse import Namespace
from importlib.metadata import EntryPoints, entry_points
from typing import AbstractSet, Any, Dict, Final, Sequence

from .common import check_empty_args, get_desc

PLUGINS_ASSESS_REPO: Final[str] = "egrader.assess_repo"
PLUGINS_ASSESS_INTER_REPO: Final[str] = "egrader.assess_inter_repo"
PLUGINS_REPORT: Final[str] = "egrader.report"


class LoadPluginError(Exception):
    """Error raised when a required plugin fails to load."""


def list_plugins(args: Namespace, extra_args: Sequence[str]):
    """List available plugins."""

    # extra_args should be empty
    check_empty_args(extra_args)

    plugin_types = (
        (":: Repository assessment plugins", PLUGINS_ASSESS_REPO),
        (":: Inter-repository assessment plugins", PLUGINS_ASSESS_INTER_REPO),
        (":: Reporting plugins", PLUGINS_REPORT),
    )

    for plugin_type in plugin_types:

        plugins: EntryPoints = entry_points(group=plugin_type[1])
        print(f"{plugin_type[0]}\n")
        for plugin in plugins:
            print(f"\t{plugin.name}\n\t\t{get_desc(plugin.load())}")
        print()


def load_plugin_functions(
    plugin_group: str, required: AbstractSet[str]
) -> Dict[str, Any]:
    """Load required plugins from the specified plugin group."""

    # Load plugins
    plugins: EntryPoints = entry_points(group=plugin_group)

    # Set of existing plugin names
    plugin_names: AbstractSet[str] = {plugin.name for plugin in plugins}

    # Are there any required plugins not in the existing plugins set?
    plugins_not_found: AbstractSet[str] = required - plugin_names
    if len(plugins_not_found) > 0:
        raise LoadPluginError(f"Required plugins {plugins_not_found} not found.")

    # Load required plugins
    plugin_functions: Dict[str, Any] = {}
    for plugin in plugins:
        if plugin.name in required:
            plugin_functions[plugin.name] = plugin.load()

    return plugin_functions


def load_plugin_function(plugin_group: str, plugin_name: str) -> Any:
    """Load a specific plugin function."""

    # Obtain the specified plugin entry point
    plugins: EntryPoints = entry_points(group=plugin_group, name=plugin_name)

    # If plugin no found, raise error
    if len(plugins) == 0:
        raise LoadPluginError(
            f"Plugin '{plugin_name}' not found in '{plugin_group}' group"
        )

    # Otherwise, return plugin function
    return plugins[0].load()
