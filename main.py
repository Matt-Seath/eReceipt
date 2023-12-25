import imaplib
import email
import dotenv
import os

dotenv.load_dotenv()

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

def main():
    imap = imaplib.IMAP4_SSL(imap_ssl_host)
    imap.login(username, password)

    imap.select("Receipts")

    _, msgnums = imap.search(None, "ALL")

    for msgnum in msgnums[0].split():
        _, data = imap.fetch(msgnum, "(RFC822)")

        message = email.message_from_bytes(data[0][1])

        msg_from = message.get('From')
        msg_to = message.get('To')
        msg_bcc = message.get('BCC')
        msg_date = message.get('Date')
        msg_subject = message.get('Subject')
        

        print(msg_to)
        print(msg_from)
        print(msg_bcc)
        print(msg_date)
        print(msg_subject)

        for part in message.walk():
            if part.get_content_type() == "text/plain":
                print(part.as_string())

        print(" ")

    imap.close()

if __name__ == "__main__":
    main()