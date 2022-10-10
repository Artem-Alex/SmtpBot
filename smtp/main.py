import sys
import smtplib
import hashlib

LOGIN = 'goreevartoum@gmail.com'
PASSWORD = 'hcvjuxfdyvccdcdh'


def main():
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login(LOGIN, PASSWORD)

    text = input("Breaking bad!\n")
    address = "artiom.goreev@yandex.ru"

    smtpObj.sendmail(LOGIN, address, text)


if __name__ == '__main__':
    sys.exit(main()) or 0
