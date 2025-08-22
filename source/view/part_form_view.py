# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/part_form_view.py

import tkinter as tk
from tkinter import ttk
from ..controller.part_form_controller import PartFormController
from ..model.part_model import PartModel

class PartFormView(tk.Toplevel):
    def __init__(self, parent, controller, pad=10):
        super().__init__(parent)
        self.part_model = PartModel()
        self.controller = PartFormController(self.part_model)
        # Nächste Sachnummer ermitteln
        self.next_number = self.part_model.get_next_partnumber()

        self.pad = pad
        
        self.title("Sachnummer anlegen")
        self.geometry("380x310")
        self.resizable(0, 0)

        self.vars = {
            "description": tk.StringVar(),
            "build_up": tk.StringVar(),
            "bom": tk.StringVar(),
            "price": tk.StringVar(),
            "sourcing_time": tk.StringVar()
        }

        self._create_widgets(self.next_number)

    def _create_widgets(self, number):
        ttk.Label(self, text="Neue Sachnummer anlegen").grid(row=0, column=0, columnspan=2, sticky="w", padx=self.pad, pady=self.pad)

        ttk.Label(self, text="Sachnummer:").grid(row=1, column=0, sticky="w", padx=self.pad)
        ttk.Label(self, text=f"{number} (autom. generiert)").grid(row=1, column=1, sticky="ew")

        ttk.Label(self, text="Bezeichnung:").grid(row=2, column=0, sticky="w", padx=self.pad)
        ttk.Entry(self, textvariable=self.vars["description"]).grid(row=2, column=1, sticky="ew")

        ttk.Label(self, text="Aufbau:").grid(row=3, column=0, sticky="w", padx=self.pad)
        ttk.Combobox(self, textvariable=self.vars["build_up"], values=["Einzelteil", "Fertigteil"]).grid(row=3, column=1, sticky="ew")

        ttk.Label(self, text="Stückliste:").grid(row=4, column=0, sticky="w", padx=self.pad)
        ttk.Combobox(self, textvariable=self.vars["bom"], values=["Ja", "Nein"]).grid(row=4, column=1, sticky="ew")

        ttk.Label(self, text="Warenwert [€]:").grid(row=5, column=0, sticky="w", padx=self.pad)
        ttk.Entry(self, textvariable=self.vars["price"]).grid(row=5, column=1, sticky="ew")

        ttk.Label(self, text="Beschaffungszeit [KW]:").grid(row=6, column=0, sticky="w", padx=self.pad)
        ttk.Entry(self, textvariable=self.vars["sourcing_time"]).grid(row=6, column=1, sticky="ew")

        ttk.Button(self, text="Eintragen", command=lambda: self._submit(number)).grid(row=7, column=0, padx=self.pad, pady=self.pad)
        ttk.Button(self, text="Abbrechen", command=self.destroy).grid(row=7, column=1, padx=self.pad, pady=self.pad)

    def _submit(self, number):
        data = {
            "number": number,
            "description": self.vars["description"].get(),
            "build_up": self.vars["build_up"].get(),
            "bom": self.vars["bom"].get(),
            "price": self.vars["price"].get(),
            "sourcing_time": self.vars["sourcing_time"].get()
        }
        if self.controller.validate_and_save(data):
            self.destroy()
