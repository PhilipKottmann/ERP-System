# Autor: Philip Kottmann
# Datum: 7.7.2025
# Beschreibung: View-Klasse

import tkinter as tk # tkinter-GUI-Modul
import re # regular expressions
from tkinter import ttk # ttk-Widgets
# Funktionalität Popup-Fenster
from tkinter.messagebox import showinfo, showwarning, showerror


class View(tk.Tk):
    def __init__(self, controller):
        super().__init__()

        # Aussenabstand allgemein
        self.PAD = 7    
        
        # Konstante Fachbereiche
        self.DEPARTMENTS = ["Vertrieb", "Disposition", "Bauteilmanagement"]

        # Definition der Laengen- und Breitenmasse des Hauptfensters:
        self.WINDOW_SIZE_TOTAL_WIDTH = 1200
        self.WINDOW_SIZE_TOTAL_HEIGHT = 800
        self.FOOTER_HEIGHT = 30
        self.main_view_height = self.WINDOW_SIZE_TOTAL_HEIGHT - self.FOOTER_HEIGHT
        
        # Spaltenbreite
        self.LEFT_COLUMN_WIDTH = 275
        self.remaining_width_without_left_column = self.WINDOW_SIZE_TOTAL_WIDTH - self.LEFT_COLUMN_WIDTH
        self.center_column_width = self.remaining_width_without_left_column/2
        self.right_column_width = self.remaining_width_without_left_column/2

        # Breite der Frames
        self.left_frame_width = self.LEFT_COLUMN_WIDTH - self.PAD
        self.center_frame_width = self.center_column_width - self.PAD
        self.right_frame_width = self.right_column_width - self.PAD

        # Klassenattribute
        self.controller = controller
        self.next_partnumber = 0
        self.customer_data = []

        # Hauptfenster wird per Unter-Methode "zusammengebaut"
        self._create_main_window()

    # main()-Methode, die das Fenster per mainloop() in Dauerschleife offenhält
    def main(self):
        self.mainloop()

    def _create_main_window(self):
        self.title("ERP-System v1.0")
        self.geometry(str(self.WINDOW_SIZE_TOTAL_WIDTH)+"x"+str(self.WINDOW_SIZE_TOTAL_HEIGHT))
        self.maxsize(self.WINDOW_SIZE_TOTAL_WIDTH, self.WINDOW_SIZE_TOTAL_HEIGHT)
        self.resizable(0,0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure((1,2), weight=1)
        self.grid_propagate(False)
    
        self._create_left_frame()
        self._create_center_frame()
        self._create_right_frame()
        self._create_footer_fame()
        self.create_listview(0, "", "")

    def _create_left_frame(self):
        self.left_frame = ttk.Frame(self, relief="groove", width=self.left_frame_width)
        self.left_frame.grid(row=0, column=0, sticky="nesw", padx=self.PAD)
        self._create_sections()

    def _create_center_frame(self):
        self.center_frame = ttk.Frame(self, relief="groove", width=self.center_frame_width)
        self.center_frame.grid(row=0, column=1, sticky="nesw", padx=self.PAD)

    def _create_right_frame(self):
        self.right_frame = ttk.Frame(self, relief="groove", width=self.right_frame_width)
        self.right_frame.grid(row=0, column=2, sticky="nesw", padx=self.PAD)

    def _create_footer_fame(self):
        self.footer_frame = ttk.Frame(self, relief="flat", padding=2)
        self.footer_frame.grid(row=1, column=0, sticky="nsew")
        self._create_copyright()
        self._end_application()

    # Erzeuge Abschnitte mit ueberschriften und Buttons:
    def _create_sections(self):
        for i in range(3):
            section = ttk.Frame(self.left_frame, relief="ridge")
            section.grid(row=i, column=0, sticky="EW", pady=self.PAD, padx=self.PAD)
            section_label = ttk.Label(section, text=self.DEPARTMENTS[i], font=("Segoe UI", 10, "bold"))
            section_label.grid(row=0, column=0, sticky="nesw", padx=self.PAD, pady=self.PAD)

            if i == 0:
                department_counter = 5 # Anzahl Buttons fuer Vertrieb
            elif i == 1:
                department_counter = 4 # Anzahl Buttons fuer Disposition
            elif i == 2:
                department_counter = 3 # Anzahl an buttons fuer Bauteilmanagement

            for j in range(department_counter):
                if i == 0 and j == 0:
                    button = ttk.Button(section, text="Kunde anlegen", command=self.add_customer_popup)
                elif i == 0 and j == 1:
                    button = ttk.Button(section, text="Auftrag anlegen", command=self.add_order_popup)
                elif i == 0 and j == 2:
                    button = ttk.Button(section, text="Auftragsbestätigung*", command=self.controller.confirm_delivery)
                elif i == 0 and j == 3:
                    button = ttk.Button(section, text="Jahresumsatz Kunde*", command=self.controller.sales_yearly_customer) 
                elif i == 0 and j == 4:
                    button = ttk.Button(section, text="Jahresumsatz Sachnummer*", command=self.controller.sales_yearly_partnumber)       
                elif i == 1 and j == 0:
                    button = ttk.Button(section, text="Bestand anzeigen", command=self.controller.show_stock)
                elif i == 1 and j == 1:
                    button = ttk.Button(section, text="Ware zubuchen", command=self.add_quantity)
                elif i == 1 and j == 2:
                    button = ttk.Button(section, text="Fehlbestände*", command=self.controller.show_shortage)
                elif i == 1 and j == 3:
                    button = ttk.Button(section, text="Mengenplanung*", command=self.controller.show_quantities_needed) 
                elif i == 2 and j == 0:
                    button = ttk.Button(section, text="Sachnummer anlegen", command=self.add_partnumber_popup)
                elif i == 2 and j == 1:
                    button = ttk.Button(section, text="Stammdaten pflegen*", command=self.controller.modify_core_data)
                elif i == 2 and j == 2:
                    button = ttk.Button(section, text="Sachnummer löschen*", command=self.controller.modify_bom)
                else:
                    button = ttk.Button(section, text=f"Button {i+1}-{j+1}")
                button.grid(row=j+1, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)

    def create_listview(self, content, heading, category):
        self.content = content
        category = category

        if self.content == 0:
            self.listbox_label = ttk.Label(self.center_frame, text="Bitte Auswahl links treffen", font=("Segoe UI", 10, "bold"))
        else:
            self.listbox_label = ttk.Label(self.center_frame, text=(heading + " (Doppelklick für Details)"), font=("Segoe UI", 10, "bold"))
        self.listbox_label.grid(row=0, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        
        self.listbox = tk.Listbox(self.center_frame, relief="ridge")
        self.listbox.config(font=("Courier", 10))
        self.listbox.grid(row=1, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)

        if self.content == 0:
            self.listbox.insert(0, "")
        else:
            heading_listbox = f"S-Nr.|Bezeichnung | {category}" # "Überschrift" der Listview-Spalten
            self.listbox.insert(0, heading_listbox)

            for item in self.content:
                row = f"{item[1]}|{item[2]}|{item[3]}"
                #self.listbox.insert(tk.END, item[1:])
                self.listbox.insert(tk.END, row)

        self.listbox.bind('<Double-Button-1>', self.get_cursor_title_double)
        # self.listbox.bind("<<ListboxSelect>>", self.get_cursor_title_single)

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

    # Anzeige der Stammdaten der Sachnummer im rechten Frame
    def show_context_partnumbers(self, partnumber):
        self.result = self.controller.read_context_partnumber(partnumber[0])

        self.lbl_heading = ttk.Label(self.right_frame, text="Detailansicht", font=("Segoe UI", 10, "bold"))
        self.lbl_heading.grid(row=0, column=0, columnspan=2, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        self.lbl_partnumber_heading = ttk.Label(self.right_frame, text="Sachnummer: ", font=("Segoe UI", 10))
        self.lbl_partnumber_heading.grid(row=1, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        self.lbl_partnumber = ttk.Label(self.right_frame, text=self.result[0][1], font=("Segoe UI", 10, "bold"))
        self.lbl_partnumber.grid(row=1, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        self.lbl_description_heading = ttk.Label(self.right_frame, text="Benennung: ", font=("Segoe UI", 10))
        self.lbl_description_heading.grid(row=2, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        self.lbl_description = ttk.Label(self.right_frame, text=self.result[0][2], font=("Segoe UI", 10, "bold"))
        self.lbl_description.grid(row=2, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        self.lbl_build_condition_heading = ttk.Label(self.right_frame, text="Aufbauzustand: ", font=("Segoe UI", 10))
        self.lbl_build_condition_heading.grid(row=3, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        self.lbl_build_condition = ttk.Label(self.right_frame, text=self.result[0][3], font=("Segoe UI", 10, "bold"))
        self.lbl_build_condition.grid(row=3, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        self.lbl_value_heading = ttk.Label(self.right_frame, text="Warenwert [€]: ", font=("Segoe UI", 10))
        self.lbl_value_heading.grid(row=4, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        self.lbl_value = ttk.Label(self.right_frame, text=self.result[0][5], font=("Segoe UI", 10, "bold"))
        self.lbl_value.grid(row=4, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        self.lbl_stock_heading = ttk.Label(self.right_frame, text="Lagerbestand [Stk.]: ", font=("Segoe UI", 10))
        self.lbl_stock_heading.grid(row=5, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        self.lbl_stock = ttk.Label(self.right_frame, text=self.result[0][9], font=("Segoe UI", 10, "bold"))
        self.lbl_stock.grid(row=5, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

        self.lbl_replacement_time_heading = ttk.Label(self.right_frame, text="Wiederbeschaffungszeit [KW]: ", font=("Segoe UI", 10))
        self.lbl_replacement_time_heading.grid(row=6, column=0, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))
        self.lbl_replacement_time = ttk.Label(self.right_frame, text=self.result[0][6], font=("Segoe UI", 10, "bold"))
        self.lbl_replacement_time.grid(row=6, column=1, sticky="EW", padx=self.PAD, pady=(self.PAD * 2))

    # Popup um Stammdaten zu ändern
    def modify_partnumber_popup(self):
        pop_up_win = tk.Toplevel()
        pop_up_win.title("Stammdaten")
        pop_up_win.geometry("250x150")
        pop_up_win.resizable(0,0)
        label = tk.Label(pop_up_win, text="Stammdaten modifizieren")
        label.grid(row=0, column=0, columnspan=2, sticky="W", padx=self.PAD, pady=self.PAD)

        self.next_partnumber = self.controller.get_next_partnumber()
        lbl_partnumber = tk.Label(pop_up_win, text="Sachnummer: ", )
        lbl_partnumber.grid(row=1, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        partnumber = tk.Label(pop_up_win, text=str(self.next_partnumber))
        partnumber.grid(row=1, column=1, sticky="W", padx=self.PAD, pady=self.PAD)

        button_close = tk.Button(pop_up_win, text="Abbrechen", command=pop_up_win.destroy)
        button_close.grid(row=2, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)
        
        button_change = tk.Button(pop_up_win, text="Ändern", command=pop_up_win.destroy)
        button_change.grid(row=2, column=1, sticky="EW", padx=self.PAD, pady=self.PAD)

    # Popup um Kundendaten einzutragen
    def add_customer_popup(self):
        self.company_name = tk.StringVar
        self.company_street = tk.StringVar
        self.company_number = tk.IntVar
        self.company_zip = tk.IntVar
        self.company_city = tk.StringVar
        self.company_phone = tk.StringVar
        self.company_email = tk.StringVar

        self.pop_up_win = tk.Toplevel()
        self.pop_up_win.title("Kunde anlegen")
        self.pop_up_win.geometry("500x280")
        self.pop_up_win.resizable(0,0)
        self.label = tk.Label(self.pop_up_win, text="Neuen Kunden anlegen")
        self.label.grid(row=0, column=0, columnspan=2, sticky="W", padx=self.PAD, pady=self.PAD)

        # Firmenname
        self.lbl_company_name = tk.Label(self.pop_up_win, text="Firmenname: ")
        self.lbl_company_name.grid(row=1, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_name = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.company_name)
        self.entry_company_name.grid(row=1, column=1, columnspan=3, sticky="EW")

        # Strasse
        self.lbl_company_street = tk.Label(self.pop_up_win, text="Straße: ")
        self.lbl_company_street.grid(row=2, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_street = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.company_street)
        self.entry_company_street.grid(row=2, column=1, sticky="W")

        # Hausnummer
        self.lbl_company_number = tk.Label(self.pop_up_win, text="Nr: ")
        self.lbl_company_number.grid(row=2, column=2, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_number = ttk.Entry(self.pop_up_win, justify="left", width=5, textvariable=self.company_number)
        self.entry_company_number.grid(row=2, column=3, sticky="EW")

        # PLZ
        self.lbl_company_zip = tk.Label(self.pop_up_win, text="PLZ: ")
        self.lbl_company_zip.grid(row=3, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_zip = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.company_zip)
        self.entry_company_zip.grid(row=3, column=1, sticky="EW")

        # Ort
        self.lbl_company_city = tk.Label(self.pop_up_win, text="Ort: ")
        self.lbl_company_city.grid(row=3, column=2, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_city = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.company_city)
        self.entry_company_city.grid(row=3, column=3, sticky="EW")

        # Telefon
        self.lbl_company_phone = tk.Label(self.pop_up_win, text="Telefon: ")
        self.lbl_company_phone.grid(row=4, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_phone = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.company_phone)
        self.entry_company_phone.grid(row=4, column=1, columnspan=3, sticky="EW")

        # E-Mail
        self.lbl_company_email = tk.Label(self.pop_up_win, text="E-Mail: ")
        self.lbl_company_email.grid(row=5, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_company_email = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.company_email)
        self.entry_company_email.grid(row=5, column=1, columnspan=3, sticky="EW")         
        
        self.btn_insert = tk.Button(self.pop_up_win, text="Eintragen", command=self.insert_customer)
        self.btn_insert.grid(row=6, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)
        
        self.button_change = tk.Button(self.pop_up_win, text="Abbrechen", command=self.pop_up_win.destroy)
        self.button_change.grid(row=6, column=1, sticky="EW", padx=self.PAD, pady=self.PAD)

    # Kundendaten in Datenbank schreiben
    def insert_customer(self):
        customer_data = [self.entry_company_name.get().strip(),
                        self.entry_company_street.get().strip(),
                        self.entry_company_number.get(),
                        self.entry_company_zip.get(),
                        self.entry_company_city.get().strip(),
                        self.entry_company_phone.get(),
                        self.entry_company_email.get().strip()]
        
        # Abfangen von Fehleingaben
        try:
            if int(self.entry_company_zip.get()) and (len(str(self.entry_company_zip.get())) == 5):
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.entry_company_email.get().strip()):  
                    if self.controller.add_customer(customer_data):
                        self.pop_up_win.destroy()
                        tk.messagebox.showinfo("Erfolg", "Kunde erfolgreich angelegt!")
                    else:
                        tk.messagebox.showerror("Fehler", "Keine Kundendaten vorhanden!")        
                        self.pop_up_win.destroy()
                else:
                    tk.messagebox.showwarning("Fehleingabe", "Falsches E-Mail-Format\n>>test@example.com")        
            else:
                tk.messagebox.showwarning("Fehleingabe", "PLZ: 5-stellige Ganzzahl")        
        except ValueError:
            tk.messagebox.showwarning("Fehleingabe", "PLZ: 5-stellige Ganzzahl")        

    # Popup um Sachnummer anzulegen
    def add_partnumber_popup(self):
        self.partnumber = self.controller.get_next_partnumber()
        self.description = tk.StringVar
        self.build_up_status = ["Einzelteil", "Fertigteil"]
        self.bom = ["Ja", "Nein"]
        self.piece_price = tk.IntVar
        self.sourcing_time = tk.IntVar

        self.pop_up_win = tk.Toplevel()
        self.pop_up_win.title("Sachnummer anlegen")
        self.pop_up_win.geometry("380x310")
        self.pop_up_win.resizable(0,0)
        self.label = tk.Label(self.pop_up_win, text="Neue Sachnummer anlegen")
        self.label.grid(row=0, column=0, columnspan=2, sticky="W", padx=self.PAD, pady=self.PAD)

        # Sachnummer - automatisch generiert
        self.lbl_partnumber = tk.Label(self.pop_up_win, text="Sachnummer: ")
        self.lbl_partnumber.grid(row=1, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_partnumber_auto = ttk.Label(self.pop_up_win, text=f"{self.partnumber}\t(autom. generiert)")
        self.entry_partnumber_auto.grid(row=1, column=1, columnspan=2, sticky="EW")

        # Bezeichnung
        self.lbl_description = tk.Label(self.pop_up_win, text="Bezeichnung: ")
        self.lbl_description.grid(row=2, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_description = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.description)
        self.entry_description.grid(row=2, column=1, columnspan=2, sticky="EW")

        # Aufbauzustand
        self.lbl_build_up_status = tk.Label(self.pop_up_win, text="Aufbau: ")
        self.lbl_build_up_status.grid(row=3, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_menu_build_up_status = ttk.Combobox(self.pop_up_win, values=self.build_up_status)
        self.entry_menu_build_up_status.set("Bitte Auswahl treffen")
        self.entry_menu_build_up_status.grid(row=3, column=1, columnspan=2, sticky="EW")

        # Stückliste
        self.lbl_bom = tk.Label(self.pop_up_win, text="Stückliste: ")
        self.lbl_bom.grid(row=4, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_menu_bom_status = ttk.Combobox(self.pop_up_win, values=self.bom)
        self.entry_menu_bom_status.set("Bitte Auswahl treffen")
        self.entry_menu_bom_status.grid(row=4, column=1, columnspan=2, sticky="EW")

        # Warenwert
        self.lbl_piece_price = tk.Label(self.pop_up_win, text="Warenwert [€]: ")
        self.lbl_piece_price.grid(row=5, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_piece_price = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.piece_price)
        self.entry_piece_price.grid(row=5, column=1, columnspan=3, sticky="EW")

        # Wiederbeschaffungszeit
        self.lbl_sourcing_time = tk.Label(self.pop_up_win, text="Beschaffungszeit [KW]: ")
        self.lbl_sourcing_time.grid(row=6, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_sourcing_time = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.sourcing_time)
        self.entry_sourcing_time.grid(row=6, column=1, columnspan=3, sticky="EW")         
        
        self.btn_insert = tk.Button(self.pop_up_win, text="Eintragen", command=self.insert_partnumber)
        self.btn_insert.grid(row=7, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)
        
        self.button_change = tk.Button(self.pop_up_win, text="Abbrechen", command=self.pop_up_win.destroy)
        self.button_change.grid(row=7, column=1, sticky="EW", padx=self.PAD, pady=self.PAD)

    # Sachnummer in Datenbank eintragen
    def insert_partnumber(self):
        partnumber_data = [ 
            self.partnumber,
            self.entry_description.get().strip(),
            self.entry_menu_build_up_status.get(),
            self.entry_menu_bom_status.get(),
            self.entry_piece_price.get().strip(),
            self.entry_sourcing_time.get().strip()]
        
        # Abfangen von Fehleingaben
        try:
            if int(self.entry_piece_price.get().strip()):
                try:
                    if int(self.entry_sourcing_time.get().strip()):
                        self.controller.add_partnumber(partnumber_data)
                        self.pop_up_win.destroy()
                        tk.messagebox.showinfo("Erfolg", "Sachnummer erfolgreich eingetragen!")
                except ValueError:
                    tk.messagebox.showwarning("Fehleingabe", "Beschaffungszeit muss eine Ganzzahl sein") 
        except ValueError:
            tk.messagebox.showwarning("Fehleingabe", "Warenwert muss eine Ganzzahl sein") 

    # Ware zum bestand zubuchen
    def add_quantity(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]-1
            if index < 0:
                tk.messagebox.showwarning("Fehler", "Bitte Sachnummer aus Liste wählen")
                return
            else:
                self.partnumber = self.content[index]
        else:
            tk.messagebox.showwarning("Fehler", "Bitte zuerst Auswahl in Bestand treffen")
            return

        self.current_quantity = self.controller.get_quantity(self.partnumber[0])
        self.new_quantity = tk.IntVar

        self.pop_up_win = tk.Toplevel()
        self.pop_up_win.title("Ware zubuchen")
        self.pop_up_win.geometry("350x200")
        self.pop_up_win.resizable(0,0)
        self.label = tk.Label(self.pop_up_win, text="Lieferung einbuchen")
        self.label.grid(row=0, column=0, columnspan=2, sticky="W", padx=self.PAD, pady=self.PAD)

        # Sachnummer anzeigen - automatisch generiert
        self.lbl_partnumber = tk.Label(self.pop_up_win, text="Sachnummer: ")
        self.lbl_partnumber.grid(row=1, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_partnumber_auto = ttk.Label(self.pop_up_win, text=f"{self.partnumber[1]}")
        self.entry_partnumber_auto.grid(row=1, column=1, columnspan=2, sticky="W")

        self.lbl_current_quantity = tk.Label(self.pop_up_win, text="aktueller Bestand: ")
        self.lbl_current_quantity.grid(row=2, column=0, sticky="W", padx=self.PAD, pady=self.PAD)

        self.entry_current_quantity = tk.Label(self.pop_up_win, text=self.current_quantity)
        self.entry_current_quantity.grid(row=2, column=1, sticky="W", padx=self.PAD, pady=self.PAD)

        self.lbl_new_quantity = tk.Label(self.pop_up_win, text="Zuzubuchende Anzahl: ")
        self.lbl_new_quantity.grid(row=3, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_new_quantity = ttk.Entry(self.pop_up_win, justify="left", textvariable=self.new_quantity)
        self.entry_new_quantity.grid(row=3, column=1, columnspan=3, sticky="EW")

        self.btn_insert = tk.Button(self.pop_up_win, text="Einbuchen", command=self.add_new_quantity)
        self.btn_insert.grid(row=4, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)
        
        self.button_change = tk.Button(self.pop_up_win, text="Abbrechen", command=self.pop_up_win.destroy)
        self.button_change.grid(row=4, column=1, sticky="EW", padx=self.PAD, pady=self.PAD)

    def add_new_quantity(self):
        self.new_quantity = int(self.entry_new_quantity.get().strip())
        try:
            if int(self.new_quantity):
                self.controller.add_quantity(self.partnumber[0], self.new_quantity)
                self.pop_up_win.destroy()
                tk.messagebox.showinfo("Erfolg", f"{self.new_quantity} Stk. zugebucht!")
        except ValueError:
            tk.messagebox.showwarning("Fehler", "Anzahl muss eine Ganzzahl sein!")

    # Popup um Auftrag anzulegen
    def add_order_popup(self):
        quantity = tk.IntVar
        self.customers = self.controller.select_customer_for_orders()
        customers_list = [customer for _, customer in self.customers]

        self.partnumbers = self.controller.select_partnumber_for_orders()
        partnumbers_list = [(partnumber, description) for _, partnumber, description in self.partnumbers]

        self.pop_up_win = tk.Toplevel()
        self.pop_up_win.title("Auftrag anlegen")
        self.pop_up_win.geometry("330x200")
        self.pop_up_win.resizable(0,0)
        self.label = tk.Label(self.pop_up_win, text="Neuen Kundenauftrag anlegen")
        self.label.grid(row=0, column=0, columnspan=2, sticky="W", padx=self.PAD, pady=self.PAD)

        # Auswahl Kunde
        self.lbl_customer = tk.Label(self.pop_up_win, text="Kunde: ")
        self.lbl_customer.grid(row=1, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_menu_customer = ttk.Combobox(self.pop_up_win, values=customers_list)
        self.entry_menu_customer.set("Bitte Auswahl treffen")
        self.entry_menu_customer.grid(row=1, column=1, columnspan=2, sticky="EW")

        # Auswahl Sachnummer
        self.lbl_partnumber_orders = tk.Label(self.pop_up_win, text="Sachnummer: ")
        self.lbl_partnumber_orders.grid(row=2, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_menu_partnumber_orders = ttk.Combobox(self.pop_up_win, values=partnumbers_list)
        self.entry_menu_partnumber_orders.set("Bitte Auswahl treffen")
        self.entry_menu_partnumber_orders.grid(row=2, column=1, columnspan=2, sticky="EW")

        # Eingabe Anzahl der Position
        self.lbl_order_pos_quantity = tk.Label(self.pop_up_win,text="Anzahl [Stk.]: ")
        self.lbl_order_pos_quantity.grid(row=3, column=0, sticky="W", padx=self.PAD, pady=self.PAD)
        self.entry_order_pos_quantity = ttk.Entry(self.pop_up_win, justify="left", textvariable=quantity)
        self.entry_order_pos_quantity.grid(row=3, column=1, columnspan=2, sticky="EW")

        self.btn_insert = tk.Button(self.pop_up_win, text="Eintragen", command=self.add_order)
        self.btn_insert.grid(row=4, column=0, sticky="EW", padx=self.PAD, pady=self.PAD)
        
        self.button_abort = tk.Button(self.pop_up_win, text="Abbrechen", command=self.pop_up_win.destroy)
        self.button_abort.grid(row=4, column=1, sticky="EW", padx=self.PAD, pady=self.PAD)

    # Auftrag in Datenbank eintragen
    def add_order(self):
        index_customer = self.entry_menu_customer.current()
        kundID = self.customers[index_customer][0]

        index_partnumber = self.entry_menu_partnumber_orders.current()
        sNrID = self.partnumbers[index_partnumber][0]

        quantity = self.entry_order_pos_quantity.get()

        try:
            if int(quantity):
                order_number = self.controller.add_order(kundID, sNrID, quantity)
                self.pop_up_win.destroy()
                tk.messagebox.showinfo("Erfolg", f"Auftrag Nr. {order_number} erfolgreich angelegt!")
        except ValueError:
            tk.messagebox.showwarning("Fehler", "Anzahl muss eine Ganzzahl sein!")

    def clear_right_frame_for_refresh(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def _create_entry(self):
        entry = ttk.Entry(self.left_frame, justify="left", textvariable=self.value_var)
        entry.grid(row=0, column=0, sticky="nsew")

    # Methode um Message-Box aufzurufen
    def show_message_box(self, title, message):
        tk.messagebox.showinfo(title=title, message=message)

    # Inhalt Fußzeile
    def _create_copyright(self):
        label = ttk.Label(self, text="© Philip Kottmann (2025)")
        label.grid(row=1, column=0, sticky="w", padx=self.PAD, pady=self.PAD)

    # Beenden-Button
    def _end_application(self):
        button = ttk.Button(self, text="Beenden", command=self.destroy)
        button.grid(row=1, column=2, sticky="e", padx=self.PAD, pady=self.PAD)