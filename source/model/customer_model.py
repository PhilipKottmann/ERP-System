# Autor: Philip Kottmann
# Datum: 22.8.2025
# Beschreibung: CustomerModel zur Bereitstellung des Kunden Models

from .base_model import BaseModel

class CustomerModel(BaseModel):
    def add_customer(self, customer_data):
        sql = "INSERT INTO kunden (firmenname, strasse, hausnummer, plz, ortsname, telefon, email) VALUES (?,?,?,?,?,?,?)"
        self.cursor.execute(sql, customer_data)
        self.connection.commit()