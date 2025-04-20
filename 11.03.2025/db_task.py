import sqlite3
from collections.abc import Collection
from typing import Iterator, Dict, Any


class TableData(Collection):
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name
        self._connection = None

    def _get_connection(self):
        if self._connection is None:
            self._connection = sqlite3.connect(self.database_name)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    def __len__(self) -> int:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        return cursor.fetchone()[0]

    def __getitem__(self, name: str) -> Dict[str, Any]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE name=?", (name,)
        )
        row = cursor.fetchone()
        if row is None:
            raise KeyError(f"No record with name '{name}' found")
        return dict(row)

    def __contains__(self, name: str) -> bool:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT 1 FROM {self.table_name} WHERE name=?", (name,)
        )
        return cursor.fetchone() is not None

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        for row in cursor:
            yield dict(row)

    def __del__(self):
        if self._connection is not None:
            self._connection.close()

if __name__ == "__main__":
    presidents = TableData(database_name='example.sqlite', table_name='presidents')

    # Get the number of presidents
    print(len(presidents))  # Outputs the current count

    # Access a specific president
    print(presidents['Yeltsin'])  # Returns Yeltsin's data as a dict

    # Check if a president exists
    print('Yeltsin' in presidents)  # True or False

    # Iterate through all presidents
    for president in presidents:
        print(president['name'])