import sqlite3 as sq


class DB:
    def __init__(self, db_name):
        self.name = db_name
        self.__db_connection = sq.connect(db_name)
        self.cur = self.__db_connection.cursor()

    def create_table(self):
        self.__db_connection.execute(
            """
                    CREATE TABLE IF NOT EXISTS client
                    (
                        token VARCHAR(255),
                        key VARCHAR(255),
                        language VARCHAR(2)
                    )
                """
        )

    def has_rows(self):
        self.cur.execute("SELECT COUNT(*) FROM client")
        return not self.cur.fetchone()[0] == 0

    def insert(self, token, key, lang='ru'):
        self.cur.execute(
            "INSERT INTO client (token, key, language) VALUES( ? , ? , ?)", (token, key, lang))
        self.__db_connection.commit()

    def update(self, token = None, key = None, lang='ru'):
        if token == None and key == None:
            self.cur.execute("UPDATE client SET language = ?", (lang,))
        else:
            self.cur.execute(
                "UPDATE client SET token = ?, key = ?, language = ?", (token, key, lang))
        self.__db_connection.commit()

    def get_data(self):
        self.cur.execute("SELECT * FROM client")
        return self.cur.fetchone()

    def __del__(self):
        if self.__db_connection != None:
            self.cur.close()
            self.__db_connection.close()
