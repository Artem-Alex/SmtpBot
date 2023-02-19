# -*- encoding: utf-8 -*-
import os
import imaplib
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())

# mail = imaplib.IMAP4_SSL('imap.gmail.com')
# mail.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))
#
# # mail.list()
# mail.select()
#
# typ, data = mail.search(None, 'ALL')
# for num in data[0].split():
#     typ, data = mail.fetch(num, '(RFC822)')
#     print('Message %s\n%s\n' % (num, data[0][1]))
# mail.close()
# mail.logout()


import imaplib


def login_credentials():
    return "mail", "password"


def connect_imap():
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    details = login_credentials()
    mail.login(os.getenv("LOGIN"), os.getenv("PASSWORD"))
    return mail


m = connect_imap()
ddate = '22-Apr-2022'
m.select("INBOX")
result, data = m.uid('search', None, '(SENTON %s)' % ddate)
print(result)
