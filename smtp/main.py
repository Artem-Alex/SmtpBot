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
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            # server.starttls(context=context)
            server.login(LOGIN, PASSWORD)
            server.sendmail(LOGIN, address, message.encode())
        except Exception as e:
            # logging.log(2, e)
            print("[Exception]", e)


if __name__ == '__main__':
    sys.exit(main()) or 0
