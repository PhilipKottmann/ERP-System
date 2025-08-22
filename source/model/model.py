# Autor: Philip Kottmann
# Datum: 7.7.2025
# Beschreibung: Model-Klasse

import sqlite3 # Datenbank-Modul
# from model.part_model import Part
from .part_model import PartModel
from .db import get_connection

class Model:
    # def __init__(self):
        # with sqlite3.connect("erp_system.db") as self.connection:
        #     self.connection.execute("PRAGMA foreign_keys = ON")
        #     self.connection.commit()
        #     self.cursor = self.connection.cursor()
    #     self.connection = get_connection()
    #     self.cursor = self.connection.cursor()
        
    # def _create_table(self, sql):
    #     self.cursor.execute(sql)
    #     self.connection.commit()

    def read_database(self):
        self.cursor.execute("SELECT * FROM sachnummern ORDER BY materialnummer ASC")
        results = self.cursor.fetchall()

    def read_all_from_database(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        self.results = self.cursor.fetchall()
        return self.results

    def read_highest_ID_from_sachnummern(self):
        self.cursor.execute("SELECT sNrID FROM sachnummern ORDER BY sNrID DESC LIMIT 1")
        last_ids = self.cursor.fetchone()
        if last_ids is None:
            return 0
        else:
            for last_id in last_ids:
                return int(last_id)
            
    def read_context_partnumber(self, partnumber):
        self.partnumber = partnumber
        self.cursor.execute(f"SELECT * FROM (sachnummern, bestaende) WHERE sachnummern.sNrID = {self.partnumber} AND bestaende.sNrID = {self.partnumber}")
        self.result = self.cursor.fetchall()
        return self.result
    
    def read_shortages(self):
        pass

    # def read_stock(self):
    #     # self.cursor.execute(f"SELECT sachnummern.sNrID, sachnummern.materialnummer, sachnummern.bezeichnung, bestaende.anzahl FROM (sachnummern, bestaende) WHERE sachnummern.sNrID = bestaende.sNrID")
    #     self.cursor.execute(f"SELECT sachnummern.sNrID, sachnummern.materialnummer, sachnummern.bezeichnung, bestaende.anzahl FROM (sachnummern, bestaende) WHERE sachnummern.sNrID = bestaende.sNrID")
    #     self.result = self.cursor.fetchall()
    #     return self.result
        
    def calculate_partnumber(self):
        basic_number = 10000    # Start der Materialnummernvergabe bei 10000
        id_to_add = self.read_highest_ID_from_sachnummern()
        return (basic_number + id_to_add + 1)

    # def add_customer(self, customer_data):
    #     self.customer = customer_data
    #     sql = "INSERT INTO kunden (firmenname, strasse, hausnummer, plz, ortsname, telefon, email) VALUES (?,?,?,?,?,?,?)"
    #     self.cursor.execute(sql, self.customer)
    #     self.connection.commit()

    # def add_partnumber(self, partnumber_data):
    #     self.partnumber_data = partnumber_data
    #     sql = "INSERT INTO sachnummern (materialnummer, bezeichnung, kennungAufbauzustand, stueckliste, warenwert, wiederbeschaffungszeit) VALUES (?,?,?,?,?,?)"
    #     self.cursor.execute(sql, self.partnumber_data)
    #     self.connection.commit()
    #     self.last_id = self.cursor.lastrowid
    #     sql = "INSERT INTO bestaende (sNrID, anzahl) VALUES (?,?)"
    #     self.cursor.execute(sql, [self.last_id, "0"])
    #     self.connection.commit()

    def get_current_quantity(self, partnumber):
        sql = f"SELECT anzahl FROM bestaende WHERE bestaende.sNrID = {partnumber}"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result
    
    def add_quantity(self, partnumber, quantity):
        read_current_quantity = self.get_current_quantity(partnumber)
        for current_quantity in read_current_quantity:
            current_quantity = current_quantity
        quantity_to_add = quantity
        new_quantity = current_quantity + quantity_to_add
        sql = f"UPDATE bestaende SET anzahl = {new_quantity} WHERE sNrID = {partnumber}"
        self.cursor.execute(sql)
        self.connection.commit()

    def add_order(self, kundID, sNrID, quantity):
        sql_orders = f"INSERT INTO auftraege (auftragseingang, auftragsabschluss, kundID, lieferID) VALUES (date('now'), NULL, {kundID}, NULL)"
        lastID = self.cursor.execute(sql_orders).lastrowid

        sql_orders = f"INSERT INTO auftragspositionen (aufID, sNrID, anzahl) VALUES ({lastID}, {sNrID}, {quantity})"
        self.cursor.execute(sql_orders)
        
        self.connection.commit()
        return lastID
    
    def select_customers_for_order(self):
        sql = "SELECT kundID, firmenname FROM kunden ORDER BY firmenname"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
    
    def select_partnumbers_for_order(self):
        sql = "SELECT sNrID, materialnummer, bezeichnung FROM sachnummern"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result