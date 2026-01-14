import sqlite3
from pathlib import Path
from typing import List
from opp.models import Command


CONFIG_DIR = Path.home() / ".config" / "opp"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class CommandRepository:
    def __init__(self, db_path: Path = CONFIG_DIR / "commandsopp.db"):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(str(self.db_path))

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alias TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL
                )
            """)

    def add_command(self, cmd: Command) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO commands (alias, name, path) VALUES (?, ?, ?)",
                (cmd.alias, cmd.name, cmd.path)
            )
            return cursor.lastrowid

    def get_by_alias(self, alias: str) -> Command | None:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, alias, name, path FROM commands WHERE alias = ?",
                (alias,)
            )
            row = cursor.fetchone()
            if row:
                return Command(
                    alias=row[1],
                    name=row[2],
                    path=row[3],
                    id=row[0]
                )
            return None
    
    def get_by_id(self, id: int) -> Command | None:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, alias, name, path FROM commands WHERE id = ?",
                (id,)
            )
            row = cursor.fetchone()
            if row:
                return Command(
                    alias=row[1],
                    name=row[2],
                    path=row[3],
                    id=row[0]
                )
            return None

    def get_all(self) -> List[Command]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT id, alias, name, path FROM commands"
            )
            return [
                Command(
                    alias=row[1],
                    name=row[2],
                    path=row[3],
                    id=row[0]
                ) for row in cursor.fetchall()
            ]

    def delete_by_alias(self, alias: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM commands WHERE alias = ?",
                (alias,)
            )
            return cursor.rowcount > 0

    def update_command(self, cmd: Command) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE commands SET name = ?, path = ? WHERE alias = ?",
                (cmd.name, cmd.path, cmd.alias)
            )
            return cursor.rowcount > 0