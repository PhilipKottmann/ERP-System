# Autor: Philip Kottmann
# Datum: 22.8.2025
# Beschreibung: StockModel für die Lagerlogistik

from .base_model import BaseModel  

class StockModel(BaseModel):
    def __init__(self):
        super().__init__()

    def get_all_stock(self):
        sql = """
                SELECT s.sNrID, s.materialnummer, s.bezeichnung, IFNULL(b.anzahl, 0) as bestand
                FROM sachnummern s
                LEFT JOIN bestaende b ON s.sNrID = b.sNrID
                ORDER BY s.materialnummer
            """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def add_stock(self, sNrID, quantity):
        sql = "UPDATE bestaende SET anzahl = anzahl + ? WHERE sNrID = ?"
        self.cursor.execute(sql, (quantity, sNrID))
        self.connection.commit()