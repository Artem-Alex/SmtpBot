import imaplib
import email
from email.header import decode_header
import dotenv
import os
import base64

dotenv.load_dotenv(dotenv.find_dotenv())

mail_pass = os.getenv('PASSWORD')
username = os.getenv('LOGIN')
imap_server = "imap.gmail.com"

directories = ("Drafts", "INBOX", "Outbox", "Sent", "Spam", "Trash")
search_criteria = ("SEEN", "UNSEEN", "all")

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(username, mail_pass)
imap.select("INBOX")

mail_uid = imap.uid('search', "all")[1][0].split()
mail_numbers = imap.search(None, "all")[1][0].split()

num_for_view = 10
last_emails_numbers = mail_uid[-num_for_view:]

res, msg = imap.uid('fetch', last_emails_numbers[-2], '(RFC822)')
extracted_msg = email.message_from_bytes(msg[0][1])
extracted_msg_date = email.utils.parsedate_tz(extracted_msg["Date"])
extracted_msg_id = extracted_msg["Message-ID"]
extracted_msg_from = extracted_msg["Return-path"]
extracted_msg_header = decode_header(extracted_msg["Subject"])[0][0].decode()

for part in extracted_msg.walk():
    if part.get_content_maintype() == 'text' and part.get_content_subtype() == "html":
        print(part.get_payload())
        # print(base64.b64decode(part.get_payload()).decode())
