import json

def reader(filepath: str):
    f = open(filepath)
    data = json.load(f)
    
    return data