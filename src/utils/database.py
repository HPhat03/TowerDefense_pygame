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
        self.__connect = sqlite3.connect("src/data/tower_defense.db")
        self.__cursor = self.__connect.cursor()

    def select(self, query: str, params: tuple = ()) -> list[tuple]:
        self.__cursor.execute(query, params)
        return self.__cursor.fetchall()

    def execute(self, query: str, params: tuple = ()) -> bool:
        self.__cursor.execute(query, params)
        self.__connect.commit()
        return self.__cursor.rowcount > 0

    def close(self) -> None:
        self.__cursor.close()
        self.__connect.close()
