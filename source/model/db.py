# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: db-Klasse

import sqlite3 # Datenbank-Modul
from pathlib import Path

DB_FILE = Path(__file__).parent / "erp-system.db"

# Stellt immer die gleiche sqlite3.connection zur Verfügung
# Initialisiert PRAGMA foreign_keys ON und Row-Factory
def get_connection():
    if not hasattr(get_connection, "_conn"):
        connection = sqlite3.connect(
            DB_FILE,
            detect_types=sqlite3.PARSE_DECLTYPES,
            check_same_thread=False
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        get_connection._conn = connection

    return get_connection._conn