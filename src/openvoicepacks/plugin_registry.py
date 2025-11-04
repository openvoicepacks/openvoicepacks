"""Plugin management for OpenVoicepacks.

This module handles the discovery and registration of plugins.
"""

# https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/

import importlib
import logging
import pkgutil

import openvoicepacks.plugins

_logger = logging.getLogger(__name__)


def discover_plugins() -> None:
    """Discover and load all plugins in the openvoicepacks.plugins package."""
    plugins = []
    for _, name, _ in pkgutil.iter_modules(openvoicepacks.plugins.__path__):
        module = importlib.import_module(f"openvoicepacks.plugins.{name}")
        plugins.append(module)
    return plugins


def register_provider(name: str, provider: object) -> None:
    """Register provider from plugins.

    This function allows plugins to self-register their TTS providers.

    Args:
        name (str): Name of the provider.
        provider (Provider): Provider class to register.
    """
    providers[name] = provider


def register_providers() -> None:
    """Register providers from discovered plugins.

    If plugins contain a PROVIDER attribute, it is registered here.
    """
    for plugin in all_plugins:
        if hasattr(plugin, "PROVIDER"):
            provider_class = getattr(plugin, "PROVIDER")  # NOQA: B009
            providers[provider_class.provider] = provider_class


all_plugins = discover_plugins()
providers = {}

# Auto-register providers from plugins
register_providers()
