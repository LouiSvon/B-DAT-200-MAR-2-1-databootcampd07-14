import json

def load_json(filepath: str) -> dict:
    if not isinstance(filepath, str):
        raise TypeError

    with open(filepath, "r", encoding="utf-8") as f: #liiii le fichier
        content = f.read()

    print(content[:100]) #uniquement les 1OO premiers caractères
    return json.loads(content)