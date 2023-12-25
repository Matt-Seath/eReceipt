import time
from itertools import chain
import email
import imaplib
import base64
import os
import re
 
imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'juanrosario38@gmail.com'
password = 'ydfegrarzvpxwtns'

# if need to restrict mail search.
criteria = {}
uid_max = 0

def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))
    # Produce search string in IMAP format:
    #   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)
#Get any attachemt related to the new mail

#Getting the uid_max, only new email are process

#login to the imap
mail = imaplib.IMAP4_SSL(imap_ssl_host)
mail.login(username, password)
#select the folder
mail.select('inbox')

result, data = mail.uid('SEARCH', None, search_string(uid_max, criteria))
uids = [int(s) for s in data[0].split()]
if uids:
    uid_max = max(uids)
    # Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.
#Logout before running the while loop
print(uid_max)
mail.logout()
while 1:
    mail = imaplib.IMAP4_SSL(imap_ssl_host)
    mail.login(username, password)
    mail.select('inbox')
    result, data = mail.uid('search', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]

    for uid in uids:
        # Have to check again because Gmail sometimes does not obey UID criterion.
        if uid > uid_max:
            result, data = mail.uid('fetch', str(uid), '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    #message_from_string can also be use here
                    print(email.message_from_bytes(response_part[1])) #processing the email here for whatever
            uid_max = uid
mail.logout()
time.sleep(1)