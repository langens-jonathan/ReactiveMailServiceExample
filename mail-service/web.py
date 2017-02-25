import sys
import imaplib
import getpass
import email
import datetime
import uuid
import helpers
import mail_helpers
import json
from flask import request


EMAIL_ADDRESS = ""
EMAIL_PWD = ""

# /fetchMails route
# will load all mails found in the INBOX of the email address
# defined above in to the triple store
@app.route("/fetchMails")
def fetchMailMethod():

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

# /process_delta [POST]
# will monitor delta reports from the triple store
# if a reports indicates that a mail is ready to be
# sent this service will fetch all necessary information from
# the store and send the mail
@app.route("/process_delta", methods=['POST'])
def processDelta():
    # The delta will be send in the body of this request, we parse it and put the
    # result in a variable.
    delta_report = json.loads(request.data)

    # From the delta's we will be able to make out which URI's should describe
    # a mail that we will have to send. We keep all these URI's in a list.
    mails_to_send = set()

    # The predicate that describes a mail as ready for sending is:
    predicate_mail_is_ready = "http://mail.com/ready"

    # The value for that predicate that we aim for:
    value_mail_is_ready = "yes"

    # The delta report can contain more than 1 delta. We will loop over each
    # delta and then loop over the inserted triples for that delta.
    #
    # If the predicate matches our predicate and the object matches our object
    # we will add the subject to the mails_to_send list.
    for delta in delta_report['delta']:
        for triple in delta['inserts']:
            if(triple['p']['value'] == predicate_mail_is_ready):
                if(triple['o']['value'] == value_mail_is_ready):
                    mails_to_send.add (triple['s']['value'])

    # fetching and sending the mails for every URI found
    for uri in mails_to_send:
        mail = mail_helpers.load_mail(uri)
        if 'uuid' in mail.keys():
            mail_helpers.send_mail(mail, EMAIL_ADDRESS, EMAIL_PWD)
        
    return "delta processed"
