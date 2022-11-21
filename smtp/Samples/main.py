import logging
import smtplib
import ssl
import sys

from smtp.config import LOGIN, PASSWORD, PORT

address = "artiom.goreev@yandex.ru"
message = """\
Subject: Вопросы по АГПЧП

Добрый вечер, Вадим Вадимович!
 
По присланным Вами статьям мне, наконец-то, удалось поправить все опечатки в формулах (осталась одно неоднозначное место).
Можно ли завтра к Вам подойти в 12:20 — 12:30?"""


def main():

    context = ssl.create_default_context()
    # with smtplib.SMTP('smtp.gmail.com', PORT) as server:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        try:
            # server.set_debuglevel(1)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(LOGIN, PASSWORD)
            server.sendmail(LOGIN, address, message.encode())
            print("[INFO] Mail send")
        except Exception as e:
            logging.log(2, e)
            print("[Exception]", e)


if __name__ == "__main__":
    sys.exit(main()) or 0
