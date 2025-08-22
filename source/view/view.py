# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/view.py

import tkinter as tk
from tkinter import ttk
from .base_view import Baseview
from .layout_mixin import LayoutMixin
from .section_mixin import SectionMixin
from .listview_mixin import ListViewMixin
from .customer_popup import CustomerPopup
from .part_form_view import PartFormView
# from ..model.part_model import PartModel


class View(Baseview, LayoutMixin, SectionMixin, ListViewMixin):
    def __init__(self, controller):
        super().__init__(controller)
        self._create_main_window()
        self._create_sections()
        self._create_listview()
        self._create_copyright()

    # Popup um Kundendaten hinzuzufügen
    def add_customer_popup(self):
        CustomerPopup(self, self.controller, self.PAD)

    # Popup um Sachnummern hinzuzufügen
    def add_partnumber_popup(self):
        PartFormView(self, self.controller)

    # Auslesen des Zeilenindex bei Doppelklick
    def get_cursor_title_double(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]-1
            if index < 0:
                return
            else:
                partnumber = self.content[index]
                if isinstance(partnumber, str):
                    self.show_message_box("Auswahl", "Bitte Auswahl unten treffen")
                    return

                else:
                    self.show_context_partnumbers(partnumber)

    # Auslesen des Zeilenindex bei einfachem Klick ("Markieren")
    def get_cursor_title_single(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]-1
            if index < 0:
                return
            else:
                partnumber = self.content[index]
                if isinstance(partnumber, str):
                    self.show_message_box("Auswahl", "Bitte Auswahl unten treffen")
                    return

                else:
                    self.show_context_partnumbers(partnumber)

    def show_context_partnumbers(self, partnumber):
        # Frame leeren
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # Daten holen
        self.result = self.controller.read_context_partnumber(partnumber[0])
        if not self.result or not self.result[0]:
            self.show_message_box("Fehler", "Keine Daten gefunden.")
            return

        data = self.result[0]

        # Labels anzeigen
        labels = [
            ("Sachnummer:", data[1]),
            ("Benennung:", data[2]),
            ("Aufbauzustand:", data[3]),
            ("Warenwert [€]:", data[5]),
            ("Lagerbestand [Stk.]:", data[9]),
            ("Wiederbeschaffungszeit [KW]:", data[6])
        ]

        heading = ttk.Label(self.right_frame, text="Detailansicht", font=("Segoe UI", 10, "bold"))
        heading.grid(row=0, column=0, columnspan=2, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        for i, (label_text, value) in enumerate(labels, start=1):
            label = ttk.Label(self.right_frame, text=label_text, font=("Segoe UI", 10))
            label.grid(row=i, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

            value_label = ttk.Label(self.right_frame, text=value, font=("Segoe UI", 10, "bold"))
            value_label.grid(row=i, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        # Optional: Bearbeiten-Button
        edit_btn = ttk.Button(self.right_frame, text="Bearbeiten", command=lambda: self.edit_partnumber(data))
        edit_btn.grid(row=len(labels)+1, column=0, columnspan=2, pady=(self.PAD * 2))


    # Inhalt Fußzeile
    def _create_copyright(self):
        self.bottom_frame = ttk.Frame(self.footer_frame)
        self.bottom_frame.grid(row=99, column=0, columnspan=3, sticky="ew", padx=self.PAD, pady=(0, self.PAD))

        # Spaltenkonfiguration
        self.bottom_frame.columnconfigure(0, weight=0)  # Copyright
        self.bottom_frame.columnconfigure(1, weight=1)  # Leerspalte
        self.bottom_frame.columnconfigure(2, weight=0)  # Button

        # Copyright links
        copyright_label = ttk.Label(
            self.bottom_frame,
            text="© 2025 Philip Kottmann",
            font=("Segoe UI", 9),
            foreground="gray"
        )
        copyright_label.grid(row=0, column=0, sticky="w", padx=self.PAD)

        # Exit-Button rechts
        exit_button = ttk.Button(self.bottom_frame, text="Beenden", command=self._end_application)
        exit_button.grid(row=0, column=2, sticky="e", padx=self.PAD)

        # Optional: Spalte 0 fixieren, Spalte 2 fixieren
        # self.bottom_frame.columnconfigure(0, weight=0)
        # self.bottom_frame.columnconfigure(2, weight=0)

    # Beenden-Button
    def _end_application(self):
        self.quit()