"""Plug-in handling functionality."""

from argparse import Namespace
from importlib.metadata import EntryPoints, entry_points
from inspect import getdoc
from pathlib import Path
from typing import AbstractSet, Any, Dict, Final, Sequence

from .cli_lib import check_empty_args

_PLUGINS_ASSESS_REPO: Final[str] = "egrader.assess_repo"
_PLUGINS_ASSESS_INTER_REPO: Final[str] = "egrader.assess_inter_repo"
_PLUGINS_REPORT: Final[str] = "egrader.report"


def _load_plugin_functions(
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
        raise PluginLoadError(f"Required plugins {plugins_not_found} not found.")

    # Load required plugins
    plugin_functions: Dict[str, Any] = {}
    for plugin in plugins:
        if plugin.name in required:
            plugin_functions[plugin.name] = plugin.load()

    return plugin_functions


def _load_plugin_function(plugin_group: str, plugin_name: str) -> Any:
    """Load a specific plugin function."""
    # Obtain the specified plugin entry point
    plugins: EntryPoints = entry_points(group=plugin_group, name=plugin_name)

    # If plugin not found, raise error
    if plugin_name not in plugins.names:
        raise PluginLoadError(
            f"Plugin {plugin_name!r} not found in {plugin_group!r} group"  # noqa: E713
        )

    # Otherwise, return plugin function
    return plugins[plugin_name].load()


class PluginLoadError(Exception):
    """Error raised when a required plugin fails to load."""


def get_short_plugin_desc(func) -> str:
    """Get a short description of a plugin."""
    desc: str | None = getdoc(func)

    if desc is not None and len(desc) > 0:
        desc = desc.split("\n")[0]
    else:
        desc = "Unavailable"

    return desc


def load_repo_plugin_functions(required: AbstractSet[str]) -> Dict[str, Any]:
    """Load required plugins from the intra-repository plugin group."""
    return _load_plugin_functions(_PLUGINS_ASSESS_REPO, required)


def load_inter_repo_plugin_functions(required: AbstractSet[str]) -> Dict[str, Any]:
    """Load required plugins from the inter-repository plugin group."""
    return _load_plugin_functions(_PLUGINS_ASSESS_INTER_REPO, required)


def load_report_plugin_function(plugin_name: str) -> Any:
    """Load a report plugin function."""
    return _load_plugin_function(_PLUGINS_REPORT, plugin_name)


def list_plugins(assess_fp: Path, args: Namespace, extra_args: Sequence[str]):
    """List available plugins."""
    # extra_args should be empty
    check_empty_args(extra_args)

    plugin_types = (
        (":: Repository assessment plugins", _PLUGINS_ASSESS_REPO),
        (":: Inter-repository assessment plugins", _PLUGINS_ASSESS_INTER_REPO),
        (":: Reporting plugins", _PLUGINS_REPORT),
    )

    for plugin_type in plugin_types:
        plugins: EntryPoints = entry_points(group=plugin_type[1])
        print(f"{plugin_type[0]}\n")
        for plugin in plugins:
            print(f"\t{plugin.name}\n\t\t{get_short_plugin_desc(plugin.load())}")
        print()
