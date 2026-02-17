import sqlite3

def create_database(db_path: str) -> None:
    if not isinstance(db_path, str):
        raise TypeError

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS country (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laureate (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            gender TEXT,
            born TEXT,
            died TEXT,
            born_country_id INTEGER,
            died_country_id INTEGER,
            FOREIGN KEY (born_country_id) REFERENCES country(id),
            FOREIGN KEY (died_country_id) REFERENCES country(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prize (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            laureate_id INTEGER,
            category_id INTEGER,
            year INTEGER,
            affiliation_country_id INTEGER,
            FOREIGN KEY (laureate_id) REFERENCES laureate(id),
            FOREIGN KEY (category_id) REFERENCES category(id),
            FOREIGN KEY (affiliation_country_id) REFERENCES country(id)
        )
    """)

    conn.commit()
    conn.close()