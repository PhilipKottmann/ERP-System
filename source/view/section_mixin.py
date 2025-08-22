# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/section_mixin.py

import tkinter as tk
from tkinter import ttk

class SectionMixin:

    PAD = 5 # Allgemeines Padding

    SECTION_BUTTONS = {
        "Vertrieb": [
            ("Kunde anlegen", "add_customer_popup"),
            ("Auftrag anlegen", "add_order_popup"),
            ("Auftragsbestätigung*", "confirm_delivery"),
            ("Jahresumsatz Kunde*", "sales_yearly_customer"),
            ("Jahresumsatz Sachnummer*", "sales_yearly_partnumber"),
        ],
        "Disposition": [
            ("Bestand anzeigen", "show_stock"),
            ("Ware zubuchen", "add_quantity"),
            ("Fehlbestände*", "show_shortage"),
            ("Mengenplanung*", "show_quantities_needed"),
        ],
        "Bauteilmanagement": [
            ("Sachnummer anlegen", "add_partnumber_popup"),
            ("Stammdaten pflegen*", "modify_core_data"),
            ("Sachnummer löschen*", "modify_bom"),
        ]
    }

    def _create_sections(self):
        for i, department in enumerate(self.SECTION_BUTTONS.keys()):
            section = ttk.Frame(self.left_frame, relief="ridge")
            section.grid(row=i, column=0, sticky="EW", pady=self.PAD, padx=self.PAD)

            label = ttk.Label(section, text=department, font=("Segoe UI", 10, "bold"))
            label.grid(row=0, column=0, sticky="nesw", padx=self.PAD, pady=self.PAD)

            for j, (text, method_name) in enumerate(self.SECTION_BUTTONS[department]):
                command = self._resolve_command(method_name)
                button = ttk.Button(section, text=text, command=command)
                button.grid(row=j+1, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)

    def _resolve_command(self, method_name):
        # Versuche zuerst, Methode in self zu finden, dann im Controller
        if hasattr(self, method_name):
            return getattr(self, method_name)
        elif hasattr(self.controller, method_name):
            return getattr(self.controller, method_name)
        else:
            return lambda: print(f"⚠️ Methode nicht gefunden: {method_name}")