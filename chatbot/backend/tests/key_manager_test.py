# -*- coding: utf-8 -*-
"""
Test file for the KeyManager class.
"""

from src.utils.key_manager import KeyManager


def main():

    key_manager = KeyManager()
    key_manager.verify_key("GOOGLE_API_KEY")
    key_manager.verify_key("LANGSMITH_API_KEY")


if __name__ == "__main__":
    main()
