import sqlite3

class CodeGenerator:
    TOTAL_CODES = 26**5  # 11,881,376

    def __init__(self, db_file="codes.db", table_name="codes"):
        self.db_file = db_file
        self.table_name = table_name
        self._init_db()

    def _init_db(self):
        """Initialize database and set starting code if empty."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_code TEXT UNIQUE
            )
        """)
        # Initialize with AAAAA if table is empty
        c.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        if c.fetchone()[0] == 0:
            c.execute(f"INSERT INTO {self.table_name} (current_code) VALUES (?)", ("AAAA@",))
        conn.commit()
        conn.close()

    def _increment_code(self, code: str) -> str | None:
        """Increment a 5-letter code A–Z. Return None if at end (ZZZZZ)."""
        if code == "ZZZZZ":
            return None  # end reached

        letters = list(code)
        i = len(letters) - 1
        while i >= 0:
            if letters[i] != 'Z':
                letters[i] = chr(ord(letters[i]) + 1)
                break
            else:
                letters[i] = 'A'
                i -= 1
        return "".join(letters)

    def get_next_code(self) -> str | None:
        """Return the next unique code or None if no more codes available."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()

        c.execute(f"SELECT current_code FROM {self.table_name} ORDER BY id DESC LIMIT 1")
        row = c.fetchone()
        current_code = row[0]

        next_code = self._increment_code(current_code)

        if next_code is None:
            conn.close()
            return None  # reached ZZZZZ

        c.execute(f"INSERT INTO {self.table_name} (current_code) VALUES (?)", (next_code,))
        conn.commit()
        conn.close()

        return next_code

    def codes_remaining(self) -> int:
        """Return how many codes are left before exhaustion."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        used = c.fetchone()[0]
        conn.close()
        return self.TOTAL_CODES - used


# Example usage
if __name__ == "__main__":
    gen = CodeGenerator()
    for _ in range(10):
        code = gen.get_next_code()
        print(code)

    print("Codes remaining:", gen.codes_remaining())