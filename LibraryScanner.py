import os
import re
import sqlite3

class LibraryScanner:
    def __init__(self, metadata_db="metadata.db"):
        self.metadata_db = metadata_db
        self.code_pattern = re.compile(r"_([A-Z]{5})\.(pdf|epub)$", re.IGNORECASE)

    def _get_metadata(self, code: str) -> dict | None:
        conn = sqlite3.connect(self.metadata_db)
        c = conn.cursor()
        c.execute("SELECT code, title, author, date_published, category, notes FROM ebooks WHERE code = ?", (code,))
        row = c.fetchone()
        conn.close()
        if row:
            return {
                "code": row[0],
                "title": row[1],
                "author": row[2],
                "date_published": row[3],
                "category": row[4],
                "notes": row[5]
            }
        return None

    def _add_metadata(self, code: str, title: str, author: str, date_published: str, category: str, notes: str):
        conn = sqlite3.connect(self.metadata_db)
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO ebooks (code, title, author, date_published, category, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (code, title, author, date_published, category, notes))
        conn.commit()
        conn.close()

    def scan_folder(self, folder_path: str) -> list[dict]:
        results = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                match = self.code_pattern.search(file)
                if match:
                    code = match.group(1)
                    metadata = self._get_metadata(code)

                    # compute relative path (so subfolders are preserved)
                    rel_path = os.path.relpath(os.path.join(root, file), folder_path)
                    category = os.path.basename(root)
                    notes = "Notes"

                    # If metadata does not exist, add it with category and notes
                    if not metadata:
                        self._add_metadata(
                            code=code,
                            title="(Unknown Title)",
                            author="(Unknown Author)",
                            date_published="(Unknown Date)",
                            category=category,
                            notes=notes
                        )
                        metadata = {
                            "code": code,
                            "title": "(Unknown Title)",
                            "author": "(Unknown Author)",
                            "date_published": "(Unknown Date)",
                            "category": category,
                            "notes": notes
                        }

                    file_path_full = os.path.join(root, file)
                    file_size = os.path.getsize(file_path_full)
                    ext = os.path.splitext(file)[1][1:].lower()
                    results.append({
                        "file_path": file_path_full,
                        "relative_path": rel_path.replace("\\", "/"),  # safe for web
                        "file_name": file,
                        "file_ext": ext,
                        "file_size": file_size,
                        "metadata": metadata
                    })
        return results