import logging

from email_validator import validate_email, EmailNotValidError

logging.basicConfig(level=logging.INFO, filename="email.log", filemode="w")


class EmailValidator:
    @classmethod
    def validate_email(cls, email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            logging.error(f"FAIL:{e}")
            return False


if __name__ == "__main__":
    print(EmailValidator.validate_email("dskfskdnfmnkd@yandex.com"))
