import os
import sqlite3


class DB:
    def __init__(self, dir):
        self.directory = dir
        self.connection = sqlite3.connect(os.path.join(dir, "otv.db"))
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

    def find_tile(self, tile):
        dbtile = self.cursor.execute("SELECT * FROM Tiles WHERE name = ?", (os.path.basename(tile),)).fetchone()

        if dbtile is None or dbtile[2] != os.path.getmtime(tile):
            return False

        return True

    def add_tile(self, tile):
        self.cursor.execute(
            "INSERT OR REPLACE INTO Tiles (name, updated_at) VALUES ( ?, ? )",
            (os.path.basename(tile), os.path.getmtime(tile))
        )
        self.connection.commit()
