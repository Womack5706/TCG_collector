import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from pathlib import Path
from Yugioh_Compiled_Cards.Yugioh_Compiled_Cards import cards

class CardDatabaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Card Database App")
        self.iconbitmap(r"C:\TCG_collector\yugioh.ico")
        self.create_widgets()
        self.bind("<Return>", self.search_card_entered)
        self.configure_treeview()
        self.bind_keyboard_shortcuts()
        self.config_file = "config.txt"  # Configuration file to store last saved CSV file path
        self.collection_csv = None
        self.current_card_data = None  

    def create_widgets(self):
        self.create_menu()
        self.create_search_section()
        self.create_treeview()
        self.create_copyright()
        self.create_separator_buttons()
        
    def create_copyright(self):
        copyright_label = tk.Label(self, text="Copyright © 2024 K. Womack - All rights reserved.")
        copyright_label.grid(row=4, column=0, columnspan=4, pady=10)

    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        menu_items = [("Open", self.open_file, "Ctrl+O"),
                      ("Save", self.save_to_collection_dialog, "Ctrl+S"),
                      ("Save As", self.save_as_collection_dialog, "Ctrl+Shift+S"),
                      ("Exit", self.exit_app, "Ctrl+Q")]
        for label, command, shortcut in menu_items:
            self.file_menu.add_command(label=label, command=command, accelerator=shortcut)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.config(menu=self.menu_bar)

    def create_search_section(self):
        self.passcode_label = ttk.Label(self, text="Enter Card Passcode:")
        self.passcode_entry = ttk.Entry(self)
        self.search_button = ttk.Button(self, text="Search", command=self.search_card)
        self.passcode_label.grid(row=0, column=0)
        self.passcode_entry.grid(row=0, column=1)
        self.search_button.grid(row=0, column=2)

    def create_treeview(self):
        self.tree = ttk.Treeview(self, columns=("Passcode", "Name", "Status", "Attack", "Defense", "Attribute", "Database"))
        headers = ["Passcode", "Name", "Status", "Attack", "Defense", "Attribute", "Database"]
        for col in headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.tree_scroll.grid(row=1, column=3, sticky="ns")

    def configure_treeview(self):
        attributes = ['EARTH', 'WATER', 'FIRE', 'WIND', 'DARK', 'LIGHT', 'DIVINE', 'SPELL', 'TRAP']
        for attr in attributes:
            self.tree.tag_configure(attr.lower(), background=self.get_tag_color(attr))

    def get_tag_color(self, attribute):
        color_map = {'EARTH': 'tan1', 'WATER': 'deep sky blue', 'FIRE': 'orange red',
                     'WIND': 'spring green', 'DARK': 'gray25', 'LIGHT': 'ivory2', 
                     'DIVINE': 'gold', 'SPELL': 'medium purple', 'TRAP': 'tomato'}
        return color_map.get(attribute, 'white')

    def bind_keyboard_shortcuts(self):
        shortcuts = {"<Control-o>": self.open_file,
                     "<Control-s>": self.save_to_collection_dialog,
                     "<Control-S>": self.save_as_collection_dialog,
                     "<Control-q>": self.exit_app}
        for key, command in shortcuts.items():
            self.bind(key, lambda event, cmd=command: cmd())

    def search_card(self):
        passcode = self.passcode_entry.get()
        self.passcode_entry.delete(0, tk.END)
        card_data = self.search_in_database(passcode)
        if card_data:
            self.current_card_data = card_data
            self.display_card(card_data)
            self.save_to_collection(card_data)  # Save the searched card
        else:
            messagebox.showinfo("Card Not Found", "The card with the given passcode was not found.")

    def search_card_entered(self, event):
        self.search_card()

    def open_file(self):
        self.collection_csv = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if self.collection_csv:
            pass  

    def save_to_collection_dialog(self):
        if self.current_card_data:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                self.collection_csv = file_path
                self.save_to_collection(self.current_card_data, self.collection_csv)


    def save_as_collection_dialog(self):
        self.collection_csv = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if self.collection_csv:
            pass  

    def exit_app(self):
        self.destroy()

    def search_in_database(self, passcode):
        for card in cards:
            if card.get('PASSCODE') == passcode:
                return card
        return None

    def display_card(self, card_data):
        self.tree.insert("", "end", values=(
            card_data.get("PASSCODE", ""),
            card_data.get("NAME", ""),
            card_data.get("STATUS", ""),
            card_data.get("ATTACK", ""),
            card_data.get("DEFENSE", ""),
            card_data.get("ATTRIBUTE", ""),
            card_data.get("CSV_FILE", "")
        ), tags=(card_data.get("ATTRIBUTE", "").lower(),))

    def save_to_collection(self, card_data, file_path=None):
        if file_path is None:
            file_path = self.collection_csv

        headers = ["Passcode", "Name", "Status", "Attack", "Defense", "Attribute", "Database"]

        with open(file_path, mode='a', newline='', encoding='utf-8') as collection_file:
            writer = csv.DictWriter(collection_file, fieldnames=headers)

            # Check if the file is empty, then write headers
            if collection_file.tell() == 0:
                writer.writeheader()

            # Write the card data
            writer.writerow({
                "Passcode": card_data.get("PASSCODE", ""),
                "Name": card_data.get("NAME", ""),
                "Status": card_data.get("STATUS", ""),
                "Attack": card_data.get("ATTACK", ""),
                "Defense": card_data.get("DEFENSE", ""),
                "Attribute": card_data.get("ATTRIBUTE", ""),
                "Database": card_data.get("CSV_FILE", "")
            })

    def create_separator_buttons(self):
        separators = [
            ("Add 100% Holo", "100% Holo"),
            ("Add Picture Holo", "Picture Holo"),
            ("Add Name Holo", "Name Holo"),
            ("Add Common", "Common")
        ]
    
        for index, (text, separator_type) in enumerate(separators, start=1):
            ttk.Button(self, text=text, command=lambda st=separator_type: self.add_separator(st)).grid(row=5, column=index, padx=5)

    def add_separator(self, separator_type):
        with open(self.collection_csv, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([f"SEPARATOR - {separator_type}", "", "", "", "", ""])

    def load_last_cards(self):
        if self.collection_csv:
            self.tree.delete(*self.tree.get_children())  # Clear the treeview before loading new cards
            with open(self.collection_csv, mode='r', newline='', encoding='utf-8') as collection_file:
                reader = csv.DictReader(collection_file)
                for row in reader:
                    self.display_card(row)

    def save_last_card(self):
        if self.collection_csv:
            with open(self.config_file, "w") as f:
                f.write(self.collection_csv)

# Main function to run the application
if __name__ == "__main__":
    app = CardDatabaseApp()
    app.create_separator_buttons()  # Create separator buttons
    app.load_last_cards()  # Load last saved cards
    app.mainloop()
