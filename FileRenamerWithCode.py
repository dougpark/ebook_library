import os
import re
from CodeGenerator import CodeGenerator

class FileRenamerWithCode:
    def __init__(self, code_generator: CodeGenerator):
        """Takes a CodeGenerator instance to ensure uniqueness."""
        self.code_gen = code_generator
        # Regex to detect "_ABCDE" at the end of a filename (before extension)
        self.code_pattern = re.compile(r"_[A-Z]{5}$")

    def has_code(self, filename: str) -> bool:
        """Check if a filename already ends with a 5-letter code."""
        base, _ = os.path.splitext(filename)
        return bool(self.code_pattern.search(base))

    def rename_file(self, filepath: str) -> str | None:
        """
        Append the next unique code to the filename and rename the file.
        Skip if file already has a code.
        Returns the new file path, or None if skipped or no more codes available.
        """
        dir_name, file_name = os.path.split(filepath)

        # Skip if file already has a code
        if self.has_code(file_name):
            print(f"Skipping (already coded): {file_name}")
            return None

        next_code = self.code_gen.get_next_code()
        if next_code is None:
            print("No more codes available.")
            return None

        base, ext = os.path.splitext(file_name)
        new_file_name = f"{base}_{next_code}{ext}"
        new_path = os.path.join(dir_name, new_file_name)

        os.rename(filepath, new_path)
        return new_path