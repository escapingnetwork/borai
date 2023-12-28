import json
import os
import logging

DEFAULT_FILE = 'data.json'

def json_loader(entry: dict, file_name: str = DEFAULT_FILE) -> None:
    try:
        with open(file_name, "r") as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        logging.error(f"File {file_name} not found. Creating a new one.")
        data = []

    data.append(entry)

    try:
        with open(file_name, "w") as json_file:
            json.dump(data, json_file)
    except IOError as e:
        logging.error(f"Error occurred: {e}")