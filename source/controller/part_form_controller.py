# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: controller/part_form_controller.py

from tkinter import messagebox
from ..model.part_model import PartModel

class PartFormController:
    def __init__(self, model):
        # self.model = PartModel()
        self.model = model
        
    def validate_and_save(self, data):
        try:
            price = int(data["price"])
            sourcing_time = int(data["sourcing_time"])
        except ValueError:
            messagebox.showwarning("Fehleingabe", "Warenwert und Beschaffungszeit müssen Ganzzahlen sein.")
            return False

        values = (
            data["number"],
            data["description"].strip(),
            data["build_up"],
            1 if data["bom"] == "Ja" else 0,  # Umwandlung von "Ja"/"Nein" in 1/0
            int(data["price"]),
            int(data["sourcing_time"])  # Umwandlung in Ganzzahl
        )

        try:
            self.model.add_partnumber(values)
            messagebox.showinfo("Erfolg", "Sachnummer erfolgreich eingetragen!")
            return True
        except Exception as e:
            messagebox.showerror("Fehler", f"Eintrag fehlgeschlagen: {e}")
            return False
