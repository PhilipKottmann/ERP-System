# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: BaseModel zur Bereitstellung der DB-Connection und Cursor

from .db import get_connection

class BaseModel:
    def __init__(self):
        self.connection = get_connection()
        self.cursor     = self.connection.cursor()

        # Tabelle "Sachnummern"
        self.create_table("""
                            CREATE TABLE IF NOT EXISTS sachnummern (
                            sNrID                       INTEGER PRIMARY KEY AUTOINCREMENT, 
                            materialnummer              INTEGER, 
                            bezeichnung                 TEXT,
                            kennungAufbauzustand        TEXT, 
                            stueckliste                 INTEGER, 
                            warenwert                   INTEGER, 
                            wiederbeschaffungszeit      INTEGER
                          )
                          """)
    
        # Tabelle "Bestände"
        self.create_table("""
                            CREATE TABLE IF NOT EXISTS bestaende (
                            bestID                      INTEGER PRIMARY KEY AUTOINCREMENT, 
                            sNrID                       INTEGER NOT NULL,
                            anzahl                      INTEGER NOT NULL,
                            FOREIGN KEY (sNrID)
                                REFERENCES sachnummern (sNrID))
                          """)
    
        # Tabelle "Kunden"
        self.create_table("""
                            CREATE TABLE IF NOT EXISTS kunden (
                            kundID                      INTEGER PRIMARY KEY AUTOINCREMENT, 
                            firmenname                  TEXT,
                            strasse                     TEXT,
                            hausnummer                  INTEGER,
                            plz                         INTEGER,
                            ortsname                    TEXT,
                            telefon                     TEXT,
                            email                       TEXT
                          )
                          """)
    
        # Tabelle "Lieferscheine"
        self.create_table("""
                            CREATE TABLE IF NOT EXISTS lieferscheine (
                            lieferID                    INTEGER PRIMARY KEY AUTOINCREMENT, 
                            versanddatum                TEXT
                          )
                          """)
    
        # Tabelle "Auftraege"
        self.create_table("""
                            CREATE TABLE IF NOT EXISTS auftraege (
                            aufID                       INTEGER PRIMARY KEY AUTOINCREMENT, 
                            auftragseingang             TEXT,
                            auftragsabschluss           TEXT,
                            kundID                      INTEGER,
                            lieferID                    INTEGER,
                            FOREIGN KEY (kundID)
                                REFERENCES kunden (kundID),
                            FOREIGN KEY (lieferID)
                                REFERENCES lieferscheine (lieferID)
                          )
                          """)
    
        # Tabelle "Auftragspositionen"
        self.create_table("""
                          CREATE TABLE IF NOT EXISTS auftragspositionen (
                            auftrPosID                  INTEGER PRIMARY KEY AUTOINCREMENT, 
                            aufID                       INTEGER,
                            sNrID                       INTEGER,
                            anzahl                      INTEGER,
                            FOREIGN KEY (aufID)
                                REFERENCES auftraege (aufID),
                            FOREIGN KEY (sNrID)
                                REFERENCES sachnummern (sNrID)
                          )
                          """)

    def create_table(self, create_sql: str):
        self.cursor.execute(create_sql)
        self.connection.commit()
    