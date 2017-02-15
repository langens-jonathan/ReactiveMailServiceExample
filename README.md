# Hands on reactive micro service

## Build a mail handling service

My goal for this short coding session is to have a mail handling service that will allow me to list and maninpulate  mails through a JSON API REST back end. And have that service pick up when I write a mail to the database and send it automatically. You can see the result of this project at:
```
https://github.com/langens-jonathan/ReactiveMailServiceExample
```

### First using mu.semte.ch to get a head start

For this project I started with cloning the mu-project repository:
```
https://github.com/mu-semtech/mu-project
```
This will give me the CRUD endpoint I need to manipulate my mail related resources. After cloning I rename the repository to MailBox and set the remote origin to a new one. For now I will leave the README.md file as it is.

For the first block we will modify the /config/resources/domain.lisp, /config/resourecs/repository.lisp and the /config/dispatcher/dispatcher.ex files.

To add the necessary resource definitions add them to the domain.lisp file as follows:
```
(define-resource mail ()
  :class (s-prefix "example:Mail")
  :properties `((:sender :string ,(s-prefix "example:sender"))
		(:subject :string ,(s-prefix "example:subject"))
		(:content :string ,(s-prefix "example:content"))
		(:ready :string ,(s-prefix "example:ready")))
  :resource-base (s-url "http://example.com/mails/")
  :on-path "mails")
```
This will create a resource description that we can manipulate on route /mails with the following properties:
- sender
- title
- body
- ready

Then add the prefix to the repository.lisp file:
```
(add-prefix "example" "http://example.com/")
```
We are almost there for a first test! The only thing left to do is to add the /mails route to the dispatcher (for more info check the documentation on http://mu.semte.ch). To do this add the following block of code to the dispatcher.ex file:
```
  match "/mails/*path" do
      Proxy.forward conn, path, "http://resource/mails/"
  end
```

Now fire this up and lets see what we have by typing:
```
docker-compose up
```
in the a console in the project root directory. We don't have a front end yet but with a tool like postman we can make GET, PATCH and POST calls to test the backend functionality.

A GET call to http://localhost/mails produces:
```
{
  "data": [],
  "links": {
    "last": "/mails/",
    "first": "/mails/"
  }
}
```
Alright! Ok no data yet but we get back resource information.

Lets do a post to make a new mail resource:
```
URL: http://localhost/mails
Headers: {"Content-Type":"application/vnd.api+json"}
Body:
{"data":{
  "attributes":{
	"sender":"flowofcontrol@gmail.com",
	"subject":"Mu Semtech Mail Server",
	"content":"This is a test for the Mu Semtech Mail Server.",
	"ready":"no"
	},
 "type":"mails"
 }}
```
This gives us the following reponse:
```
{
  "data": {
    "attributes": {
      "sender": "flowofcontrol@gmail.com",
      "subject": "Mu Semtech Mail Server",
      "content": "This is a test for the Mu Semtech Mail Server.",
      "ready": "no"
    },
    "id": "58978C2A6460170009000001",
    "type": "mails",
    "relationships": {}
  }
}
```
That worked, in about 30 minutes we have a fully functional REST API endpoint for managing mail resources!

To verify to original get again, this now produces:
```
{
  "data": {
    "attributes": {
      "sender": "flowofcontrol@gmail.com",
      "subject": "Mu Semtech Mail Server",
      "content": "This is a test for the Mu Semtech Mail Server.",
      "ready": "no"
    },
    "id": "58978C3A6460170009000002",
    "type": "mails",
    "relationships": {}
  }
}
```

### Part 2 of the set up
Before we can start writing our reactive mail managing micro-service we will need to add a monitoring service to monitor the DB. This will be a lot easier then it sounds with mu.semte.ch. To start open the docker-compose.yml file and add the following lines at the bottom of the page:
```
  delta:
    image: semtech/mu-delta-service:beta-0.7
    links:
      - db:db
    volumes:
      - ./config/delta-service:/config
    environment:
      CONFIGFILE: "/config/config.properties"
      SUBSCRIBERSFILE: "/config/subscribers.json"
```
This will add the monitoring service to our installation. The last thing to do for now is to change the link on the resource microservice by replacing
```
    links:
      - db:database
```
with
```
    links:
      - delta:database
```
The final steps are to create the configuration and subscribers files. Create a file called config.properties at the location config/delta-service/config.properties and write the following lines in that file:
```
# made by Langens Jonathan
queryURL=http://db:8890/sparql
updateURL=http://db:8890/sparql
sendUpdateInBody=true
calculateEffectives=true
```
and then create config/delta-service/subscribers.json and put this JSON inside:
```
{
  "potentials":[
  ],
  "effectives":[
  ]
}
```
If we do drc rm and then drc up again then the delta service will be booting and already monitoring the changes that happen in the database! Of course we are not doing anything with them yet. So we will create a new micro-service just for this purpose.

## Writing your first micro-service

### Building the mail handling microservice (mail-service)

#### Objectives
The next step is to build our mail handling microservice. To do this we create a new directory called mail-service in our platform base directory. Then we create a file in that directory called 'Dockerfile'. We will start from a mu.semte.ch template to make developing this microservice that much quicker. Mu.semte.ch has templates for a bunch of languages ruby, javascript, python, ... For this microservice we will go for python 2.7. To do this we simply need to create a web.py file which will serve as the location for our code. Next add the following to the Dockerfile:
```
FROM semtech/mu-python-template

MAINTAINER Langens Jonathan <flowofcontrol@gmail.com>
```
I know it doesn't say much but it doesn't need to. The python template will handle the rest.

Then we need to add some mail manipulating functionality. Since this is not really the objective of this post I create a mail_helpers.py file and paste the following code in there:
```
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
```
As you can see the mail_helpers contain 2 functions, 1 to iterate over all emails in a mailbox and the other to save a single email to the triple store. Easy peasy!

Next we create a web.py file for more information on how the python template can be used you can visit: https://github.com/mu-semtech/mu-python-template/blob/master/README.md. I created the following method to process all mails:
```
@app.route("/fetchMails")
def fetchMailMethod():
    EMAIL_ADDRESS = "address"
    EMAIL_PWD = "pwd"

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
```
This method is rather straightforward it just opens a connection to a email address and opens the inbox mailbox. Then selects it for processing thus inserting all mails into the triple store.

End of part 1!
