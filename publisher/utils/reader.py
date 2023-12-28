import json
from typing import Any

def read_json_file(filepath: str) -> Any:
    """
    Reads a JSON file and returns the data.

    Parameters:
    filepath (str): The path to the JSON file.

    Returns:
    Any: The data from the JSON file.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {filepath}")