import sys
import imaplib
import getpass
import email
import datetime
import uuid
import helpers
import json
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders


# helper functino that saves a mail to the triple store
# it expects the following parameters:
# sender, date, subject and content and creates
# a new UUID for each mail that it saves
def save_mail(sender, date, subject, content):
    str_uuid = str(uuid.uuid4())
    insert_query = "INSERT DATA\n{\nGRAPH <http://mu.semte.ch/application>\n{\n<http://mail.com/examples/mail/" + str_uuid + "> a <http://mail.com/Mail>;\n"
    insert_query += "<http://mail.com/from> \"" + sender + "\";\n"
    insert_query += "<http://mail.com/date> \"" + date + "\";\n"
    insert_query += "<http://mail.com/content> \"" + content + "\";\n"
    insert_query += "<http://mail.com/subject> \"" + subject + "\";\n"
    insert_query += "<http://mail.com/ready> \"yes\";\n"
    insert_query += "<http://mu.semte.ch/vocabularies/core/uuid> \"" + str_uuid + "\".\n"
    insert_query += "}\n}"
    helpers.update(insert_query)
    

# helper functino that expects a python mail library
# mailbox object
# this function will call the save_mail function for
# every mail in the mailbox
def process_mailbox(mailbox):
  rv, data = mailbox.search(None, "ALL")
  if rv != 'OK':
      print "No messages found!"
      return

  for num in data[0].split():
      rv, data = mailbox.fetch(num, '(RFC822)')
      if rv != 'OK':
          print "ERROR getting message", num
          return

      msg = email.message_from_string(data[0][1])
      content = str(msg.get_payload())
      content = content.replace('\n','')
      
      save_mail(msg['From'], msg['Date'], msg['Subject'], content)

# the load mail function loads a mail from the database
# if it cannot find a mail in the database for the given
# uuid it will return nil
def load_mail(uri):
    # this query will find the mail (if it exists)
    select_query = "SELECT DISTINCT ?uuid ?from ?to ?ready ?subject ?content\n"
    select_query += "WHERE \n{\n"
    select_query += "<" + str(uri) + "> <http://mail.com/from> ?from;\n"
    select_query += "a <http://mail.com/Mail>;\n"
    select_query += "<http://mail.com/content> ?content;\n"
    select_query += "<http://mail.com/subject> ?subject;\n"
    select_query += "<http://mail.com/to> ?to;\n"
    select_query += "<http://mail.com/ready> ?ready;\n"
    select_query += "<http://mu.semte.ch/vocabularies/core/uuid> ?uuid.\n"
    select_query += "}"

    # execute the query...
    result = helpers.query(select_query)

    # if the length of the result array is 0 we return nil
    if len(result['results']['bindings']) < 1:
        return {}

    # I should probably check here but for a quick test application
    # it doesn't matter that much. If there is more than 1 result
    # that would indicate a data error
    bindings = result['results']['bindings'][0]

    # we extract an object
    mail = dict()
    mail['uuid'] = bindings['uuid']['value']
    mail['from'] = bindings['from']['value']
    mail['ready'] = bindings['ready']['value']
    mail['to'] = bindings['to']['value']
    mail['subject'] = bindings['subject']['value']
    mail['content'] = bindings['content']['value']

    return mail

# I have copied the followig function entirely from
# http://naelshiab.com/tutorial-send-email-python/
# the function has been slightly modified to take the
# dictionary mail object from load_mail into account
def send_mail(mail, email_address, email_password):
    
    fromaddr = email_address
    toaddr = mail['to']
    
    msg = MIMEMultipart()
    
    msg['From'] = mail['from']
    msg['To'] = mail['to']
    msg['Subject'] = mail['subject']
    
    body = mail['content']
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, email_password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
