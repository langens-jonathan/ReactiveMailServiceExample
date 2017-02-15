import sys
import imaplib
import getpass
import email
import datetime
import uuid
import helpers
import mail_helpers

@app.route("/fetchMails")
def fetchMailMethod():
    EMAIL_ADDRESS = "maildude.tenforce@gmail.com"
    EMAIL_PWD = "TenforceS3cr3tZ"

    MAIL_SERVER = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
        MAIL_SERVER.login(EMAIL_ADDRESS, EMAIL_PWD)
    except imaplib.IMAP4.error:
        print "Logging into mailbox failed! "

    rv, data = MAIL_SERVER.select("INBOX")
    if rv == 'OK':
        mail_helpers.process_mailbox(MAIL_SERVER)
        MAIL_SERVER.close()
                
    MAIL_SERVER.logout()

    return "ok"
