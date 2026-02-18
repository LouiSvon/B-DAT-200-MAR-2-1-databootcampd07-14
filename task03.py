import json
import sqlite3

def insert_categories(json_file: str, db_name: str) -> None:
    if not isinstance(json_file, str) or not isinstance(db_name, str):
        raise TypeError

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories = set()
    for laureate in data.get("laureates", []):
        for prize in laureate.get("prizes", []):
            cat = (prize.get("category") or "").strip()
            if cat:
                categories.add(cat)

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.executemany(
        "INSERT OR IGNORE INTO category (name) VALUES (?)",
        [(c,) for c in sorted(categories)],
    )

    conn.commit()
    conn.close()