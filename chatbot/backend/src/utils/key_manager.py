# -*- coding: utf-8 -*-
"""
File: key_manager.py

This file contains the KeyManager class, responsible for managing API keys
for the chatbot. It loads the keys from a .env file and sets them as
environment variables in the system.
"""

import os
from dotenv import load_dotenv, find_dotenv

from src.utils.logger_manager import logger


class KeyManager:
    """
    Class to manage the system's API keys. It loads the keys from a .env file
    and assigns them to the system environment.
    """

    def __init__(self, env_file: str = ".env") -> None:
        """
        Initializes the KeyManager and loads keys from the .env file.

        Args:
            env_file (str): The path to the .env file.
        """
        logger.info("Initializing KeyManager...")
        self._env_file = env_file
        self._load_keys()

    def _load_keys(self) -> None:
        """
        Private method to load API keys from the .env file.
        Raises a RuntimeError and stops execution if loading fails.
        """
        logger.info("Loading API keys from .env file...")
        logger.info(f"Current working directory: {os.getcwd()}")
        try:
            dotenv_path = find_dotenv(self._env_file)
            if not dotenv_path:
                raise FileNotFoundError(
                    f".env file not found at path: {self._env_file}"
                )
            load_dotenv(dotenv_path)
            logger.info("API keys successfully loaded.")
        except Exception as e:
            logger.error(f"Failed to load API keys: {e}")
            raise RuntimeError(f"Failed to load API keys: {e}") from e

    def verify_key(self, key_name: str) -> bool:
        """
        Verifies if a specific API key has been correctly assigned to the environment.

        Args:
            key_name (str): The name of the environment variable to verify.

        Returns:
            bool: True if the key is correctly assigned, False otherwise.
        """
        logger.info(
            f"Verifying if the API key '{key_name}' is correctly assigned in the environment..."
        )
        key_value = os.getenv(key_name)
        if key_value:
            logger.info(f"{key_name} has been correctly assigned.")
            logger.debug(
                f"Environment variable assigned: {key_name} with value: {key_value}"
            )
            return True
        else:
            logger.error(
                f"{key_name} has not been correctly assigned. Check the .env file."
            )
            return False
