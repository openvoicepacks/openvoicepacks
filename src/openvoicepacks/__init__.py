"""OpenVoicePacks"""

import logging
import os

import coloredlogs
from jinja2 import Environment, PackageLoader, select_autoescape

# import openvoicepacks.plugin_registry
from openvoicepacks.utils import metadata

# Load settings from environment variables
_loglevel = os.environ.get("OVP_LOG_LEVEL", "INFO").upper()
os.environ["PYDANTIC_ERRORS_INCLUDE_URL"] = "1"

# Remove any default handlers
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Install coloredlogs on the root logger
_LOGFORMAT = "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
coloredlogs.install(level=_loglevel, fmt=_LOGFORMAT)

# Jinja2 template environment
template_env = Environment(
    loader=PackageLoader("openvoicepacks"),
    autoescape=select_autoescape(),
)
template_env.globals = {"metadata": metadata}
