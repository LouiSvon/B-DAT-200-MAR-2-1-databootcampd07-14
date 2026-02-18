import json
import sqlite3

def insert_countries(json_file: str, db_name: str) -> None:
    if not isinstance(json_file, str) or not isinstance(db_name, str):
        raise TypeError

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    codes_to_names = {}
    affiliation_names = set()

    for laureate in data.get("laureates", []):
        b_code = (laureate.get("bornCountryCode") or "").strip()
        b_name = (laureate.get("bornCountry") or "").strip()
        if b_code and b_name:
            codes_to_names[b_code] = b_name

        d_code = (laureate.get("diedCountryCode") or "").strip()
        d_name = (laureate.get("diedCountry") or "").strip()
        if d_code and d_name:
            codes_to_names[d_code] = d_name

        for prize in laureate.get("prizes", []):
            for aff in (prize.get("affiliations") or []):
                a_name = (aff.get("country") or "").strip()
                if a_name:
                    affiliation_names.add(a_name)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("SELECT id, code, name FROM country")
    rows = cur.fetchall()

    existing_codes = {code for _, code, _ in rows if code}
    existing_names = {name for _, _, name in rows if name}

    to_insert_codes = []
    for code, name in sorted(codes_to_names.items()):
        if code not in existing_codes:
            to_insert_codes.append((code, name))
            existing_codes.add(code)
            existing_names.add(name)

    if to_insert_codes:
        cur.executemany(
            "INSERT INTO country (code, name) VALUES (?, ?)",
            to_insert_codes,
        )

    to_insert_aff = []
    for name in sorted(affiliation_names):
        if name not in existing_names:
            to_insert_aff.append((name,))
            existing_names.add(name)

    if to_insert_aff:
        cur.executemany(
            "INSERT INTO country (code, name) VALUES (NULL, ?)",
            to_insert_aff,
        )

    conn.commit()
    conn.close()