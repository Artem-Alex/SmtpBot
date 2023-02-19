import os
import logging
import sqlite3

from sqlite3 import Error

logging.basicConfig(level=logging.INFO, filename=f"{__name__}.log",
                    format="%(asctime)s %(levelname)s %(message)s")


class Database:
    @staticmethod
    def __sql_connection():
        try:
            con = sqlite3.connect("Samples/smtp_bot_database.db")
            logging.info("Database connection")
            return con

        except Error:
            logging.critical(f"The database is not connected \n {Error}", exc_info=True)

    @classmethod
    def create_mail_table(cls):

        con = cls.__sql_connection()
        cursor = con.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS mails(
            id INTEGER PRIMARY KEY,
            mail TEXT
            )""")

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

        cursor.execute(f"DELETE FROM mails where id = {user_id}")

        con.commit()
        con.close()


if __name__ == "__main__":
    print(Database.select_mail(1))
