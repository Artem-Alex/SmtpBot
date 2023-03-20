import logging
import smtplib
import ssl
import dotenv
import os


dotenv.load_dotenv(dotenv.find_dotenv())
logging.basicConfig(level=logging.INFO, filename="f{__name__}.log", filemode="w")

PORT = int(os.getenv('PORT'))
PASSWORD = os.getenv('PASSWORD')


class MessageSender:
    def __init__(
        self, login: str, address: str, message_subject: str, message_body: str
    ):
        self.__login = login
        self.__address = address
        self.__message = f"{message_subject}\n{message_body}"
        self.__smtp_address = "smtp.gmail.com"

    def __choose_smtp_address(self) -> str:
        pass

    def send_message(self):
        context = ssl.create_default_context()
        with smtplib.SMTP(self.__smtp_address, PORT) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(self.__login, PASSWORD)
            server.sendmail(self.__login, self.__address, self.__message.encode())
            logging.info("Mail send")
