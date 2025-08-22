# Autor: Philip Kottmann
# Datum: 7.7.2025
# Beschreibung: Controller-Klasse

from ..model.base_model import BaseModel # Import BaseModel-Klasse
from ..model.part_model import PartModel # Import PartModel-Klasse
from ..model.model import Model # Import Model-Klasse
from ..view.view import View # Import View-Klasse
from ..model.db import get_connection
from ..model.customer_model import CustomerModel

class Controller:
    def __init__(self):
        self.model = BaseModel()
        self.customer_model = CustomerModel()
        self.view = View(self)
        self.next_partnumber = 0
        self.current_partnumber = 0
        self.current_quantity = 0

    def add_customer(self, customer_data):
        self.customer_model.add_customer(customer_data)
        return True

    def confirm_delivery(self):
        self.view.clear_right_frame_for_refresh()
        self.view.show_message_box("Lieferbestätigung", "Dummy: Lieferung bestätigt!")

    def sales_yearly_customer(self):
        self.view.clear_right_frame_for_refresh()
        self.view.show_message_box("Kundenumsatz", "Dummy: Jahresumsatz nach Kunde")

    def sales_yearly_partnumber(self):
        self.view.clear_right_frame_for_refresh()
        self.view.show_message_box("Sachnummernumsatz", "Dummy: Jahresumsatz nach Sachnummer")

    def select_customer_for_orders(self):
        return self.model.select_customers_for_order()
    
    def select_partnumber_for_orders(self):
        return self.model.select_partnumbers_for_order()

    def show_shortage(self):
        self.view.clear_right_frame_for_refresh()
        #self.view.create_listview(0, "Fehlbestände/Mindermengen", "Best.")
        self.view.show_message_box("Fehlbestände", "Dummy: Fehlbestände")

    def show_quantities_needed(self):
        self.view.show_message_box("Mengenplanung", "Dummy: Mengenplanung")

    def show_stock(self):
        self.result = self.model.read_stock()
        self.view.create_listview(self.result, "Lagerbestände", "Best.")

    def modify_bom(self):
        self.view.clear_right_frame_for_refresh()
        self.view.show_message_box("Sachnmummer löschen", "Dummy: Sachnummer gelöscht")

    def modify_core_data(self):
        self.view.clear_right_frame_for_refresh()
        self.view.show_message_box("Stammdaten pflegen", "Dummy: Stammdaten pflegen")

    def read_content_listview(self, table):
        return self.model.read_all_from_database(table)
    
    def read_context_partnumber(self, partnumber):
        return self.model.read_context_partnumber(partnumber)
    
    def add_quantity(self, partnumber, quantity):
        self.model.add_quantity(partnumber, quantity)

    def add_order(self, kundID, sNrID, quantity):
        return self.model.add_order(kundID, sNrID, quantity)
        
    # SETTER:
    def set_next_partnumber(self):
        self.next_partnumber = self.model.calculate_partnumber()

    # GETTER:
    def get_next_partnumber(self):
        self.set_next_partnumber()
        return self.next_partnumber
    
    def get_quantity(self, partnumber):
        self.partnumber = partnumber
        return self.model.get_current_quantity(self.partnumber)
    
    def division_method(zaehler, nenner):
        return zaehler / nenner
        

# # Aufruf der main()-Methode, sobald das Programm aus controller.py aufgerufen wird
# if __name__ == "__main__":
#     erp_system = Controller()
#     erp_system.main()