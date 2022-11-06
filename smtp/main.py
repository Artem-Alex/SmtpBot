import logging
import smtplib
import ssl
import sys

LOGIN = 'goreevartoum@gmail.com'
PASSWORD = 'hcvjuxfdyvccdcdh'
PORT = 587

address = "artiom.goreev@yandex.ru"
# text = input("[Template] Breaking bad!\n")
message = """\
Subject: Привет!
[Template] Это письмо было отправлено из Python."""


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


if __name__ == '__main__':
    sys.exit(main()) or 0
