import json

def display_info() -> None:
    with open("./nobels.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = set()  #set stocker les catégories sans doublons
    names = set()
    countries = set()

    for laureate in data.get("laureates", []): #récupère le prénom
        firstname = (laureate.get("firstname") or "").strip()
        surname = (laureate.get("surname") or "").strip()
        full_name = f"{firstname} {surname}".strip()
        if full_name:
            names.add(full_name)

        code = (laureate.get("bornCountryCode") or "").strip()
        country = (laureate.get("bornCountry") or "").strip()
        if code and country:
            countries.add((code, country))

        for prize in laureate.get("prizes", []):
            category = (prize.get("category") or "").strip()
            if category:
                categories.add(category)

    print(sorted(categories))
    print(sorted(names))
    print(sorted(countries))