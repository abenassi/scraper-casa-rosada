import os
import re

# Directory containing the files
directory = "./discursos/scraped_data"

# Regular expression to match the current file naming pattern
pattern = re.compile(r"(\d+)_\w+_(\d{2})_de_(\w+)_de_(\d{4})\.txt")

# Mapping of month names in Spanish to their respective numbers
months = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}

# Iterate over files in the directory
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        file_id, day, month_name, year = match.groups()
        month = months[month_name.lower()]
        new_filename = f"{year}_{month}_{day}_{file_id}.txt"
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)
        os.rename(old_file, new_file)
        print(f"Renamed: {filename} -> {new_filename}")
