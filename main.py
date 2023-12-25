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
    print(username)
    print(password)

if __name__ == "__main__":
    main()