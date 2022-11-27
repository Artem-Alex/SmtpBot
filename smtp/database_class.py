import sqlite3

from sqlite3 import Error


class Database:
    @staticmethod
    def __sql_connection():
        try:
            con = sqlite3.connect("smtp_bot_database.db")
            return con

        except Error:
            print(Error)

    @classmethod
    def create_mail_table(cls):

        con = cls.__sql_connection()
        cursor = con.cursor()

        cursor.execute("CREATE TABLE mails(id integer PRIMARY KEY, mail text)")

        con.commit()
        con.close()

    @classmethod
    def insert_mail(cls, user_id: int, mail: str):

        con = cls.__sql_connection()
        cursor = con.cursor()

        cursor.execute(f"INSERT INTO mails(id, mail) VALUES(?, ?)", (user_id, mail))

        con.commit()
        con.close()

    @classmethod
    def update_mail(cls, user_id: int, mail: str):

        con = cls.__sql_connection()
        cursor = con.cursor()

        cursor.execute(f"UPDATE mails SET mail = {mail} where id = {user_id}")

        con.commit()
        con.close()

    @classmethod
    def select_mail(cls, user_id: int) -> str:

        con = cls.__sql_connection()
        cursor = con.cursor()

        cursor.execute(f"SELECT mail FROM mails where id = {user_id}")

        rows = cursor.fetchall()
        con.close()

        return None if len(rows) == 0 else rows[0][0]

    @classmethod
    def delete_mail(cls, user_id: int):

        con = cls.__sql_connection()
        cursor = con.cursor()

        cursor.execute(f"DELETE mail FROM mails where id = {user_id}")

        con.commit()
        con.close()


if __name__ == "__main__":
    print(Database.select_mail(1))
