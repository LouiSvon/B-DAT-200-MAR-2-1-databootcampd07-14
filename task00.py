import json

def load_json(filepath: str) -> dict:
    if not isinstance(filepath, str):
        raise TypeError

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    print(content[:100])
    return json.loads(content)