import sqlite3


class Database:
    """A class to manage database connections and queries.

    Methods:
        select(query: str, params: tuple = ()) -> list[tuple]:
            Executes a SELECT query and returns the result.
        execute(query: str, params: tuple = ()) -> bool:
            Executes a non-SELECT query and returns True if successful.
        close() -> None: Closes the database connection and cursor.
    """

    def __init__(self):
        self.connect = sqlite3.connect("data/tower_defense.db")
        self.cursor = self.connect.cursor()

    def select(self, query: str, params: tuple = ()) -> list[tuple]:
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def execute(self, query: str, params: tuple = ()) -> bool:
        self.cursor.execute(query, params)
        self.connect.commit()
        return self.cursor.rowcount > 0

    def close(self) -> None:
        self.cursor.close()
        self.connect.close()

