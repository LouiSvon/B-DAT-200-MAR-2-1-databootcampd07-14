from task00 import load_json

def display_info() -> None:
    data = load_json("./nobels.json")

    categories = set() #set stocker les catégories sans doublons
    names = set()
    countries = set()

    for laureate in data.get("laureates", []):
>
        firstname = laureate.get("firstname", "") or "" #récupère le prénom
        surname = laureate.get("surname", "") or ""
        full_name = f"{firstname} {surname}".strip()
        if full_name:
            names.add(full_name)

        code = laureate.get("bornCountryCode", "") or ""
        country = laureate.get("bornCountry", "") or ""
        code = code.strip()
        country = country.strip()
        if code and country:
            countries.add((code, country))

        for prize in laureate.get("prizes", []):
            category = (prize.get("category", "") or "").strip()
            if category:
                categories.add(category)

    print(sorted(categories))
    print(sorted(names))
    print(sorted(countries))