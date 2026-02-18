import json
import sqlite3

def _normalize_date(value):
    if not isinstance(value, str):
        return None
    value = value.strip()
    if value == "" or value == "0000-00-00":
        return None
    return value

def insert_laureates(json_file: str, db_name: str) -> None:
    if not isinstance(json_file, str) or not isinstance(db_name, str):
        raise TypeError

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute("SELECT id, code, name FROM country")
    rows = cur.fetchall()

    code_to_id = {}
    name_to_id = {}
    for cid, code, name in rows:
        if code:
            code_to_id[code] = cid
        if name:
            name_to_id[name] = cid

    def resolve_country_id(code, name):
        code = (code or "").strip()
        name = (name or "").strip()
        if code and code in code_to_id:
            return code_to_id[code]
        if name and name in name_to_id:
            return name_to_id[name]
        return None

    to_insert = []
    for laureate in data.get("laureates", []):
        firstname = (laureate.get("firstname") or "").strip()
        surname = (laureate.get("surname") or "").strip()
        full_name = f"{firstname} {surname}".strip() if surname else firstname

        gender = (laureate.get("gender") or "").strip() or None
        born = _normalize_date(laureate.get("born"))
        died = _normalize_date(laureate.get("died"))

        born_country_id = resolve_country_id(
            laureate.get("bornCountryCode"),
            laureate.get("bornCountry"),
        )
        died_country_id = resolve_country_id(
            laureate.get("diedCountryCode"),
            laureate.get("diedCountry"),
        )

        to_insert.append(
            (full_name, gender, born, died, born_country_id, died_country_id)
        )

    cur.executemany(
        """
        INSERT INTO laureate (name, gender, born, died, born_country_id, died_country_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        to_insert,
    )

    conn.commit()
    conn.close()