from email_validator import validate_email, EmailNotValidError


class EmailValidator:
    @classmethod
    def validate_email(cls, email: str) -> bool:
        try:
            validate_email(email, check_deliverability=False)
            return True
        except EmailNotValidError as e:
            print(f"FAIL:{e}")
            return False


if __name__ == "__main__":
    print(EmailValidator.validate_email("goreevartdsoums@yandex.com"))
