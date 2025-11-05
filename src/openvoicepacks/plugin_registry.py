"""Plugin management for OpenVoicepacks.

This module handles the discovery and registration of plugins.

Each plugin can register one or more TTS providers by defining a PROVIDER attribute
pointing to a subclass of the Provider base class.

Attributes:
    providers (dict): A registry of available TTS providers.
"""

# https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/

import importlib
import pkgutil

import openvoicepacks.plugins

# Registry of providers, keyed by provider name. Import this to access provider list.
providers = {}


def discover_plugins() -> None:
    """Discover and load all plugins in the openvoicepacks.plugins package."""
    plugins = []
    for _, name, _ in pkgutil.iter_modules(openvoicepacks.plugins.__path__):
        module = importlib.import_module(f"openvoicepacks.plugins.{name}")
        plugins.append(module)
    return plugins


def register_providers() -> None:
    """Register providers from discovered plugins.

    If plugins contain a PROVIDER attribute, it is registered here.
    """
    for plugin in all_plugins:
        if hasattr(plugin, "PROVIDER"):
            provider_class = getattr(plugin, "PROVIDER")  # NOQA: B009
            providers[provider_class.provider] = provider_class


# Auto-register plugins and providers
all_plugins = discover_plugins()
register_providers()
