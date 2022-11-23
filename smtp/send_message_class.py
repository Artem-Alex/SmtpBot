import smtplib
import ssl
import string

from smtp.config import LOGIN, PASSWORD, PORT


class MessageSender:
    def __init__(self, address: string, message: string):
        self.__address = address
        self.__message = message
        self.__smtp_address = "smtp.gmail.com"

    def __choose_smtp_address(self) -> string:
        pass

    def send_message(self):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.__smtp_address, PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(LOGIN, PASSWORD)
            server.sendmail(LOGIN, self.__address, self.__message.encode())
            print("[INFO] Mail send")
