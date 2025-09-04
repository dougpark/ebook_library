import os
import re

root_dir = "ebooks"
pattern = re.compile(r"^(.*)_([A-Z]{5})$")

for folder, _, files in os.walk(root_dir):
    for filename in files:
        name, ext = os.path.splitext(filename)
        match = pattern.match(name)
        if match:
            new_name = match.group(1) + ext
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} -> {new_path}")