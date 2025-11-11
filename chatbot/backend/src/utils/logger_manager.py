# -*- coding: utf-8 -*-
"""
File: logger_manager.py

Configures the global logger for the application using Loguru.
The logger outputs to the console with color and a custom format.
"""

from loguru import logger

import sys
from src.config.config_init import LOGGER_LEVEL

# Remove any previous Loguru configuration (if any)
logger.remove()

# Logger configuration to print to the console with colors and custom format
logger.add(
    sys.stdout,  # Destination: standard console
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{module}:{function}:{line}</cyan> - {message}",  # Log format
    level=LOGGER_LEVEL,  # Nivel de log modular desde config
    colorize=True,  # Colorize the logs
    backtrace=True,  # Show full stacktrace for errors
    diagnose=True,  # Additional diagnostics for exceptions
)

logger.debug("Logger configured successfully.")

# From here, any class or module that imports this file
# will have access to the globally configured logger.
