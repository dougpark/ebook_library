import sqlite3

class MetadataDB:
    def __init__(self, db_file="metadata.db"):
        self.db_file = db_file
        self._init_db()

    def _init_db(self):
        """Initialize the metadata database with the ebooks table and new columns."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS ebooks (
                code TEXT PRIMARY KEY,
                title TEXT,
                author TEXT,
                date_published TEXT,
                category TEXT,
                notes TEXT
            )
        """)
        # Add new columns if they don't exist (for migrations)
        c.execute("PRAGMA table_info(ebooks)")
        columns = [row[1] for row in c.fetchall()]
        if "category" not in columns:
            c.execute("ALTER TABLE ebooks ADD COLUMN category TEXT")
        if "notes" not in columns:
            c.execute("ALTER TABLE ebooks ADD COLUMN notes TEXT")
        conn.commit()
        conn.close()

    def add_entry(self, code: str, title: str, author: str, date_published: str, category: str = None, notes: str = None):
        """Add a new ebook entry to the metadata database."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            INSERT INTO ebooks (code, title, author, date_published, category, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (code, title, author, date_published, category, notes))
        conn.commit()
        conn.close()

    def update_entry(self, code: str, title: str, author: str, date_published: str, category: str = None, notes: str = None):
        """Update an existing ebook entry in the metadata database."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("""
            UPDATE ebooks
            SET title = ?, author = ?, date_published = ?, category = ?, notes = ?
            WHERE code = ?
        """, (title, author, date_published, category, notes, code))
        conn.commit()
        conn.close()

    def get_entry(self, code: str) -> dict | None:
        """Retrieve an ebook entry by code."""
        conn = sqlite3.connect(self.db_file)
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

    def list_all(self) -> list[dict]:
        """List all ebook entries."""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT code, title, author, date_published, category, notes FROM ebooks ORDER BY code")
        rows = c.fetchall()
        conn.close()
        return [
            {
                "code": r[0],
                "title": r[1],
                "author": r[2],
                "date_published": r[3],
                "category": r[4],
                "notes": r[5]
            }
            for r in rows
        ]