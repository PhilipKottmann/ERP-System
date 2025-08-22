# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: model/part_model.py

from .base_model import BaseModel

class PartModel(BaseModel):
    def __init__(self):
        super().__init__()

    def add_partnumber(self, data):
        sql =   """
                INSERT INTO sachnummern 
                (materialnummer, bezeichnung, kennungAufbauzustand, stueckliste, warenwert, wiederbeschaffungszeit) 
                VALUES (?,?,?,?,?,?)
                """
        
        self.cursor.execute(sql, data)
        self.connection.commit()
        return self.cursor.lastrowid
    
    def get_all_partnumbers(self):
        sql =   """
                SELECT * FROM sachnummern ORDER BY materialnummer
                """
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def get_next_partnumber(self):
        sql =   """
                SELECT materialnummer FROM sachnummern ORDER BY materialnummer DESC LIMIT 1
                """
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        return (row["materialnummer"] + 1) if row else 10000
