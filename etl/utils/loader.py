import json
import os

FILE = 'data.json'

def json_loader(
        entry: dict,
        file: str = FILE,
) -> None:
    with open(file, "r+") as file:
        data = json.load(file)
        data.append(entry)
        file.seek(0)
        json.dump(data, file)