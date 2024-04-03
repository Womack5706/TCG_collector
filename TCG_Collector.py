import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from pathlib import Path

class CardDatabaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Card Database App")
        self.iconbitmap("C:/Yugioh/yugioh_collection/yugioh.ico")  # Set the icon for the main window
        self.create_widgets()
        self.bind("<Return>", self.search_card_entered)
        self.configure_treeview()
        self.bind_keyboard_shortcuts()
        self.last_row_index = self.load_last_row_index()  # Load last row index
        self.collection_csv = "C:/Yugioh/collection/Collection.csv"  # Default collection CSV

    def create_widgets(self):
        self.create_menu()
        self.create_search_section()
        self.create_treeview()
        self.create_copyright()
        self.create_separator_buttons()  # Add the separator buttons

    def load_last_row_index(self):
        try:
            with open("last_row_index.txt", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_last_row_index(self, index):
        with open("last_row_index.txt", "w") as f:
            f.write(str(index))

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
        self.tree = ttk.Treeview(self, columns=("Name", "Status", "Attack", "Defense", "Attribute", "Database"))
        headers = ["Name", "Status", "Attack", "Defense", "Attribute", "Database"]
        for col in headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree_scroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.tree_scroll.grid(row=1, column=3, sticky="ns")

    def configure_treeview(self):
        attributes = ['earth', 'water', 'fire', 'wind', 'dark', 'light', 'divine']
        for attr in attributes:
            self.tree.tag_configure(attr, background=self.get_tag_color(attr))

    def bind_keyboard_shortcuts(self):
        shortcuts = {"<Control-o>": self.open_file,
                     "<Control-s>": self.save_to_collection_dialog,
                     "<Control-S>": self.save_as_collection_dialog,
                     "<Control-q>": self.exit_app}
        for key, command in shortcuts.items():
            self.bind(key, lambda event, cmd=command: cmd())

    def search_card(self):
        passcode = self.passcode_entry.get()
        if passcode:
            card_data = self.search_in_csv(passcode)
            if card_data:
                self.display_card(card_data)
                self.save_to_collection(card_data, self.collection_csv)  # Save to default collection CSV
            else:
                messagebox.showinfo("Card Not Found", "The card with the given passcode was not found.")
        else:
            messagebox.showinfo("No Passcode", "Please enter a passcode.")

    def search_card_entered(self, event):
        self.search_card()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            pass  # Placeholder for file opening logic

    def save_to_collection_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.save_to_collection(card_data, file_path)

    def save_as_collection_dialog(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            pass  # Placeholder for file saving logic

    def exit_app(self):
        self.save_last_row_index(self.last_row_index)  # Save last row index before exiting
        self.destroy()

    def search_in_csv(self, passcode):
        card_data = None
        databases_dir = Path("C:/yugioh_cardlist_scraper/data/en/")
        for database_file in databases_dir.glob("*.csv"):
            with open(database_file, newline='', encoding='utf-8') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    if row.get('Passcode') == passcode:
                        card_data = row
                        card_data['Database'] = database_file.stem
                        return card_data
        return card_data

    def create_copyright(self):
        copyright_label = tk.Label(self, text="© K.W. 2024")
        copyright_label.grid(row=2, column=0, columnspan=4, sticky="se")

    def get_tag_color(self, attribute):
        color_map = {'earth': 'tan1', 'water': 'deep sky blue', 'fire': 'orange red',
                     'wind': 'spring green', 'dark': 'gray25', 'light': 'ivory2', 'divine': 'gold'}
        return color_map.get(attribute, 'white')

    def display_card(self, card_data):
        self.tree.insert("", "end", values=(
            card_data.get("Name", ""),
            card_data.get("Status", ""),
            card_data.get("attack", ""),
            card_data.get("defense", ""),
            card_data.get("Attribute", ""),
            card_data.get("Database", "")
        ), tags=(card_data.get("Attribute", ""),))

    def save_to_collection(self, card_data, file_path):
        if card_data:
            with open(file_path, mode='a', newline='', encoding='utf-8') as collection_file:
                writer = csv.writer(collection_file)
                writer.writerow([card_data.get(header, '') for header in self.tree["columns"]])
            # Update the last row index
            self.last_row_index += 1

    def create_separator_buttons(self):
        separator_frame = ttk.Frame(self)
        separator_frame.grid(row=1, column=4, sticky="nsew", padx=10, pady=10)

        ttk.Label(separator_frame, text="Card Separators", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2)

        separator_options = ["100% Holos", "Picture Holos", "Name Holos", "Common (None Holo)"]
        shortcut_keys = ["1", "2", "3", "4"]

        for i, (separator, shortcut) in enumerate(zip(separator_options, shortcut_keys)):
            btn = ttk.Button(separator_frame, text=f"{separator} ({shortcut})", command=lambda sep=separator: self.add_separator(sep))
            btn.grid(row=i + 1, column=0, padx=5, pady=5)

    def add_separator(self, separator):
        # Implement the function to add the specified separator to the CSV file
        pass  # Placeholder for separator functionality

if __name__ == "__main__":
    app = CardDatabaseApp()
    app.mainloop()
