# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/base_view.py

import tkinter as tk

class Baseview(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        # Controller-Referenz
        self.controller = controller

        # Allgemeine Konfiguration
        self.PAD = 5    # Aussenabstand allgemein     
        
        # Fenstergroesse
        self.WINDOW_SIZE_TOTAL_WIDTH = 1200
        self.WINDOW_SIZE_TOTAL_HEIGHT = 800
        self.FOOTER_HEIGHT = 30
        self.main_view_height = self.WINDOW_SIZE_TOTAL_HEIGHT - self.FOOTER_HEIGHT
        
        # Spaltenbreiten
        self.LEFT_COLUMN_WIDTH = 275
        self.remaining_width_without_left_column = self.WINDOW_SIZE_TOTAL_WIDTH - self.LEFT_COLUMN_WIDTH
        self.center_column_width = self.remaining_width_without_left_column/2
        self.right_column_width = self.remaining_width_without_left_column/2

        # Frame-Breiten
        self.left_frame_width = self.LEFT_COLUMN_WIDTH - self.PAD
        self.center_frame_width = self.center_column_width - self.PAD
        self.right_frame_width = self.right_column_width - self.PAD

        # Weitere Attribute
        self.next_partnumber = 0
        self.customer_data = []