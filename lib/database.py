import sqlite3

class DataBase:
    def __init__(self, path) -> None:
        self.path = path

    def getCursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def execute(self, cursor, sql):
        return cursor.execute(sql)

    def executeMany(self, cursor, sql, data):
        return cursor.executemany(sql, data)

    def fetchAll(self, result):
        return result.fetchall()

    def fetchOne(self, result):
        return result.fetchone()

    def close(self):
        print(f"""Closing {self.path} database""")
        self.connection.close()

    def open(self):
        print(f"""Opening {self.path} database""")
        self.connection = sqlite3.connect(self.path)

        # allowing foreign keys
        self.connection.execute("PRAGMA foreign_keys = 1")

    def drop(self, table):
        self.execute(self.getCursor(), f"""DROP TABLE {table}""")
        print("Deleted table ", table)

    def deleteData(self, table):
        self.execute(self.getCursor(), f"""DELETE FROM {table}""")
        print("Deleted all record from ", table)
        self.commit()

