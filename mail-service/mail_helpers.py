import sys
import imaplib
import getpass
import email
import datetime
import uuid
import helpers

def save_mail(sender, date, subject, content):
    str_uuid = str(uuid.uuid4())
    insert_query = "INSERT DATA\n{\nGRAPH <http://mu.semte.ch/application>\n{\n<http://mail.com/examples/mail/" + str_uuid + "> a <http://mail.com/Mail>;\n"
    insert_query += "<http://mail.com/from> \"" + sender + "\";\n"
    insert_query += "<http://mail.com/date> \"" + date + "\";\n"
    insert_query += "<http://mail.com/content> \"" + content + "\";\n"
    insert_query += "<http://mail.com/subject> \"" + subject + "\";\n"
    insert_query += "<http://mu.semte.ch/vocabularies/core/uuid> \"" + str_uuid + "\".\n"
    insert_query += "}\n}"
    print "query:\n", insert_query
    helpers.update(insert_query)
    

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
