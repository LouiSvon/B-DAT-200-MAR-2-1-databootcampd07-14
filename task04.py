import json
import sqlite3

def insert_countries(json_file: str, db_name: str) -> None:
    if not isinstance(json_file, str) or not isinstance(db_name, str):
        raise TypeError

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    coded_countries = {}
    affiliation_countries = set()

    for laureate in data.get("laureates", []):
        b_code = (laureate.get("bornCountryCode") or "").strip()
        b_name = (laureate.get("bornCountry") or "").strip()
        if b_code and b_name:
            coded_countries[b_code] = b_name

        d_code = (laureate.get("diedCountryCode") or "").strip()
        d_name = (laureate.get("diedCountry") or "").strip()
        if d_code and d_name:
            coded_countries[d_code] = d_name

        for prize in laureate.get("prizes", []):
            for aff in prize.get("affiliations", []) or []:
                a_name = (aff.get("country") or "").strip()
                if a_name:
                    affiliation_countries.add(a_name)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.executemany(
        "INSERT OR IGNORE INTO country (code, name) VALUES (?, ?)",
        [(code, name) for code, name in sorted(coded_countries.items())],
    )

    cur.execute("SELECT name FROM country WHERE name IS NOT NULL")
    existing_names = {row[0] for row in cur.fetchall() if row and row[0]}

    to_insert = sorted([name for name in affiliation_countries if name not in existing_names])
    cur.executemany(
        "INSERT INTO country (code, name) VALUES (NULL, ?)",
        [(name,) for name in to_insert],
    )

    conn.commit()
    conn.close()