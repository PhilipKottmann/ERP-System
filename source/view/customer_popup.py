# Autor: Philip Kottmann
# Datum: 3.8.2025
# Beschreibung: view/customer_popup.py

import tkinter as tk
import re
from tkinter import ttk
from tkinter import messagebox

class CustomerPopup:
    def __init__(self, root, controller, pad):
        self.root = root
        self.controller = controller
        self.PAD = pad

        self.company_name = tk.StringVar()
        self.company_street = tk.StringVar()
        self.company_number = tk.StringVar()
        self.company_zip = tk.StringVar()
        self.company_city = tk.StringVar()
        self.company_phone = tk.StringVar()
        self.company_email = tk.StringVar()

        self._create_popup()

    def _create_popup(self):
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

        insert_btn = ttk.Button(self.pop_up_win, text="Eintragen", command=self._insert_customer)
        insert_btn.grid(row=6, column=0, padx=self.PAD, pady=self.PAD)

        cancel_btn = ttk.Button(self.pop_up_win, text="Abbrechen", command=self.pop_up_win.destroy)
        cancel_btn.grid(row=6, column=1, padx=self.PAD, pady=self.PAD)

    def _insert_customer(self):
        name = self.company_name.get()
        street = self.company_street.get()
        number = int(self.company_number.get())
        zip_code = int(self.company_zip.get())
        city = self.company_city.get()
        phone = self.company_phone.get()
        email = self.company_email.get()

        customer_data = [name, street, number, zip_code, city, phone, email]

        # Abfangen von Fehleingaben
        try:
            if int(self.entry_company_zip.get()) and (len(str(self.entry_company_zip.get())) == 5):
                if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.entry_company_email.get().strip()):  
                    if self.controller.add_customer(customer_data):
                        self.pop_up_win.destroy()
                        messagebox.showinfo("Erfolg", "Kunde erfolgreich angelegt!")
                    else:
                        messagebox.showerror("Fehler", "Keine Kundendaten vorhanden!")        
                        self.pop_up_win.destroy()
                else:
                    messagebox.showwarning("Fehleingabe", "Falsches E-Mail-Format\n>>test@example.com")        
            else:
                messagebox.showwarning("Fehleingabe", "PLZ: 5-stellige Ganzzahl")        
        except ValueError:
            messagebox.showwarning("Fehleingabe", "PLZ: 5-stellige Ganzzahl")  