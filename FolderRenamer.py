import os
from FileRenamerWithCode import FileRenamerWithCode
from CodeGenerator import CodeGenerator

class FolderRenamer:
    def __init__(self, code_generator: CodeGenerator):
        """Uses FileRenamerWithCode to rename all ebook files in a folder."""
        self.file_renamer = FileRenamerWithCode(code_generator)

    def rename_folder(self, folder_path: str) -> list[str]:
        """
        Scan folder (including subfolders) for .pdf and .epub files
        and rename them with unique codes.

        Returns a list of renamed file paths.
        """
        renamed_files = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith((".pdf", ".epub")):
                    old_path = os.path.join(root, file)
                    new_path = self.file_renamer.rename_file(old_path)
                    if new_path:
                        renamed_files.append(new_path)

        return renamed_files