"""
Various utility functions.
"""
import json
from pathlib import Path


def load_config() -> dict:
    """
    Loads the configuration file.
    :return: configuration information
    """
    return load_json(Path('data/config.json'))


def load_keys() -> dict:
    """
    Loads the API credentials.
    :return: api credentials
    """
    return load_json(Path('data/keys.json'))


def load_json(path: Path):
    """
    Loads authentification keys/tokens.
    :param path: JSON file to load the keys from
    :return: Dictionary containing the key-file information
    """
    with open(path, mode='r', encoding='utf8') as file:
        return json.load(file)
