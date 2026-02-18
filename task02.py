import sqlite3

def create_database(db_path: str) -> None:
    if not isinstance(db_path, str):
        raise TypeError

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT,
            name TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS laureate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            born DATE,
            died DATE,
            bornCountry_id INTEGER,
            diedCountry_id INTEGER,
            FOREIGN KEY (bornCountry_id) REFERENCES country(id),
            FOREIGN KEY (diedCountry_id) REFERENCES country(id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS prize (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laureate_id INTEGER,
            category_id INTEGER,
            motivation TEXT,
            year INTEGER,
            affiliation_id INTEGER,
            FOREIGN KEY (laureate_id) REFERENCES laureate(id),
            FOREIGN KEY (category_id) REFERENCES category(id),
            FOREIGN KEY (affiliation_id) REFERENCES country(id)
        )
    """)

    conn.commit()
    conn.close()