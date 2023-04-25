from abc import ABC, abstractmethod
import sqlite3 as sq


class DataBase(ABC):

    @abstractmethod
    def update(self):
        ...
    
    @abstractmethod
    def select(self):
        ...

class SqliteDB(DataBase):
    def __init__(self, db_name) -> None:
        self.name = db_name
        self._db_connection = sq.connect(db_name)
        self.cur = self._db_connection.cursor()

    def update(self, ID, token, key, lang):
        self.cur.execute(
            "INSERT OR REPLACE INTO client(ID, token, key, language) VALUES(?, ? , ? , ?)", (ID, token, key, lang))
        self._db_connection.commit()
        
    def select(self, ID):
        self.cur.execute(
            "SELECT token, key, language FROM client WHERE ID=?", (ID,)
        )
        return self.cur.fetchone()
