from pathlib import Path
import sqlite3


class DB:
    def __init__(self, directory):
        self.database = Path(directory, "otv.db")
        self.connection = sqlite3.connect(str(self.database))
        self.cursor = self.connection.cursor()
        self.create()

    def create(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS Tiles (
                id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                name   TEXT UNIQUE,
                updated_at DOUBLE ); 
            CREATE UNIQUE INDEX IF NOT EXISTS idx_tiles_name ON Tiles(name);
    """)

    def tiles(self):
        return self.cursor.execute("SELECT * FROM Tiles;").fetchall()

    def find_tile(self, input_tile):
        tile = Path(input_tile)

        dbtile = self.cursor.execute("SELECT * FROM Tiles WHERE name = ?", (tile.name,)).fetchone()

        if dbtile is None or dbtile[2] != tile.stat().st_mtime:
            return False

        return True

    def add_tile(self, input_tile):
        tile = Path(input_tile)
        
        self.cursor.execute(
            "INSERT OR REPLACE INTO Tiles (name, updated_at) VALUES ( ?, ? )",
            (tile.name, tile.stat().st_mtime)
        )
        self.connection.commit()
