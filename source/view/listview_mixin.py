# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/listview_mixin.py

import tkinter as tk
from tkinter import ttk

class ListViewMixin:
    def _create_listview(self):
        # Haupt-Frame im center_frame platzieren
        self.list_frame = ttk.Frame(self.center_frame)
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=self.PAD, pady=self.PAD)

        # Label oben links
        self.list_label = ttk.Label(self.list_frame, text="Auswahl", font=("Segoe UI", 11, "bold"))
        self.list_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, self.PAD))

        # Listbox mit Scrollbar
        self.listbox = tk.Listbox(self.list_frame, font=("Segoe UI", 10))
        self.listbox.grid(row=1, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Grid-Konfiguration für responsives Verhalten
        self.list_frame.rowconfigure(1, weight=1)
        self.list_frame.columnconfigure(0, weight=1)

    def update_listview(self, items, title="Auswahl"):
        self.list_label.config(text=title)
        self.listbox.delete(0, "end")
        for item in items:
            self.listbox.insert("end", item)
