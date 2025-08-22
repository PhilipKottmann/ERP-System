# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/layout_mixin.py

from tkinter import ttk

class LayoutMixin:
    def _create_main_window(self):
        self.title("ERP-System v1.0")
        self.geometry(str(self.WINDOW_SIZE_TOTAL_WIDTH)+"x"+str(self.WINDOW_SIZE_TOTAL_HEIGHT))
        self.maxsize(self.WINDOW_SIZE_TOTAL_WIDTH, self.WINDOW_SIZE_TOTAL_HEIGHT)
        self.resizable(0,0)

        # Grid-Konfiguration
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure((1,2), weight=1)
        self.grid_propagate(False)

        # Frames erstellen
        self._create_left_frame()
        self._create_center_frame()
        self._create_right_frame()
        self._create_footer_fame()
        # self.create_listview(0, "", "")

    def _create_left_frame(self):
        self.left_frame = ttk.Frame(self, relief="groove", width=self.left_frame_width)
        self.left_frame.grid(row=0, column=0, sticky="nesw", padx=self.PAD)
        #self._create_sections()

    def _create_center_frame(self):
        self.center_frame = ttk.Frame(self, relief="groove", width=self.center_frame_width)
        self.center_frame.grid(row=0, column=1, sticky="nesw", padx=self.PAD)

    def _create_right_frame(self):
        self.right_frame = ttk.Frame(self, relief="groove", width=self.right_frame_width)
        self.right_frame.grid(row=0, column=2, sticky="nesw", padx=self.PAD)

    def _create_footer_fame(self):
        self.footer_frame = ttk.Frame(self, relief="flat", padding=2)
        self.footer_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        self.footer_frame.columnconfigure(0, weight=1)