import csv
from pathlib import Path

# Directory containing CSV files
csv_directory = Path("C:/yugioh_cardlist_scraper/data/en/")

# Output file path
output_file = "C:/TCG_collector/Yugioh_Compiled_Cards/Yugioh_Compiled_Cards.py"

# List to store cards
cards = []

# Iterate over each CSV file in the directory
for csv_file in csv_directory.glob("*.csv"):
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        # Iterate over each row in the CSV file
        for row in reader:
            # Extract desired attributes
            attribute = row.get("ATTRIBUTE", row.get("attribute", "")).capitalize()  # Read both lowercase and uppercase attributes and capitalize the first letter
            attack = row.get("ATTACK", row.get("attack", "")) if attribute not in ["Spell", "Trap"] else ""  # Ignore if attribute is Spell or Trap
            defense = row.get("DEFENSE", row.get("defense", "")) if attribute not in ["Spell", "Trap"] else ""  # Ignore if attribute is Spell or Trap
            card = {
                "Passcode": row.get("PASSCODE", row.get("Passcode", "")),
                "Name": row.get("NAME", row.get("Name", "")),
                "Status": row.get("STATUS", row.get("Status", "")),
                "Attribute": row.get("Attribute", ""),
                "Attack": attack,
                "Defense": defense,
                "CSV_File": csv_file.name  # Store the name of the CSV file
            }
            cards.append(card)

# Write compiled cards to a Python source dictionary file
with open(output_file, "w", encoding="utf-8") as out_file:
    out_file.write("# Compiled Card Data\n\n")
    out_file.write("cards = [\n")
    for card in cards:
        # Output all keys with uppercase
        card_uppercase = {k.upper(): v for k, v in card.items()}
        out_file.write("    " + str(card_uppercase) + ",\n")
    out_file.write("]\n")
