# Hands on reactive micro service - Part 2

## Build a mail handling service

My goal for this short coding session is to have a mail handling service that will allow me to list and maninpulate  mails through a JSON API REST back end. And have that service pick up when I write a mail to the database and send it automatically. You can see the result of this project at:
```
https://github.com/langens-jonathan/ReactiveMailServiceExample


## Tutorial in 2 parts

This tutorial was written in 2 parts (part 1 and part 2), you can find part 1 here: https://mu.semte.ch/2017/02/16/reactive-microservice-hands-on-tutorial-part-1/

In the first part we set up a mu.semte.ch base project, configured it for use as a mail handling service and added a delta service to the basic project setup.

## The delta service
The delta service's responsibilities are:
* acting as the SPARQL endpoint for the microservices
* calculating the differences (deltas) that a query will introduce in the database
* notifying interested parties of these differences

For this hands on we use version beta-0.8 of the delta service.

### How do these delta reports look like?

There are 2 types of delta reports, you have potential inserts and effective inserts. A report for either will look like:
```
{
  "query": "PREFIX+example%3A+%3Chttp%3A%2F%2Fexample.com%2F%3E%0APREFIX+ext%3A+%3Chttp%3A%2F%2Fmu.semte.ch%2Fvocabularies%2Fext%2F%3E%0APREFIX+rm%3A+%3Chttp%3A%2F%2Fmu.semte.ch%2Fvocabularies%2Flogical-delete%2F%3E%0APREFIX+typedLiterals%3A+%3Chttp%3A%2F%2Fmu.semte.ch%2Fvocabularies%2Ftyped-literals%2F%3E%0APREFIX+mu%3A+%3Chttp%3A%2F%2Fmu.semte.ch%2Fvocabularies%2Fcore%2F%3E%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0APREFIX+app%3A+%3Chttp%3A%2F%2Fmu.semte.ch%2Fapp%2F%3E%0APREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0APREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0AINSERT+DATA+%0A%7B%0A++++GRAPH+%3Chttp%3A%2F%2Fmu.semte.ch%2Fapplication%3E+%7B%0A++++++++%3Chttp%3A%2F%2Fexample.com%2Fmails%2F58B187FA6AA88E0009000001%3E+a+example%3AMail.%0A++++%3Chttp%3A%2F%2Fexample.com%2Fmails%2F58B187FA6AA88E0009000001%3E+mu%3Auuid+%2258B187FA6AA88E0009000001%22.%0A++++%3Chttp%3A%2F%2Fexample.com%2Fmails%2F58B187FA6AA88E0009000001%3E+example%3Asender+%22flowofcontrol%40gmail.com%22.%0A++++%3Chttp%3A%2F%2Fexample.com%2Fmails%2F58B187FA6AA88E0009000001%3E+example%3Asubject+%22Mu+Semtech+Mail+Server%22.%0A++++%3Chttp%3A%2F%2Fexample.com%2Fmails%2F58B187FA6AA88E0009000001%3E+example%3Acontent+%22This+is+a+test+for+the+Mu+Semtech+Mail+Server.%22.%0A++++%3Chttp%3A%2F%2Fexample.com%2Fmails%2F58B187FA6AA88E0009000001%3E+example%3Aready+%22no%22.%0A%7D%0A%7D%0A",
  "delta": [
    {
      "type": "effective",
      "graph": "http://mu.semte.ch/application",
      "inserts": [
        {
          "s": {
            "value": "http://example.com/mails/58B187FA6AA88E0009000001",
            "type": "uri"
          },
          "p": {
            "value": "http://example.com/subject",
            "type": "uri"
          },
          "o": {
            "value": "Mu Semtech Mail Server",
            "type": "literal"
          }
        },
        {
          "s": {
            "value": "http://example.com/mails/58B187FA6AA88E0009000001",
            "type": "uri"
          },
          "p": {
            "value": "http://example.com/ready",
            "type": "uri"
          },
          "o": {
            "value": "no",
            "type": "literal"
          }
        },
        {
          "s": {
            "value": "http://example.com/mails/58B187FA6AA88E0009000001",
            "type": "uri"
          },
          "p": {
            "value": "http://mu.semte.ch/vocabularies/core/uuid",
            "type": "uri"
          },
          "o": {
            "value": "58B187FA6AA88E0009000001",
            "type": "literal"
          }
        },
        {
          "s": {
            "value": "http://example.com/mails/58B187FA6AA88E0009000001",
            "type": "uri"
          },
          "p": {
            "value": "http://example.com/content",
            "type": "uri"
          },
          "o": {
            "value": "This is a test for the Mu Semtech Mail Server.",
            "type": "literal"
          }
        },
        {
          "s": {
            "value": "http://example.com/mails/58B187FA6AA88E0009000001",
            "type": "uri"
          },
          "p": {
            "value": "http://example.com/sender",
            "type": "uri"
          },
          "o": {
            "value": "flowofcontrol@gmail.com",
            "type": "literal"
          }
        },
        {
          "s": {
            "value": "http://example.com/mails/58B187FA6AA88E0009000001",
            "type": "uri"
          },
          "p": {
            "value": "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            "type": "uri"
          },
          "o": {
            "value": "http://example.com/Mail",
            "type": "uri"
          }
        }
      ],
      "deletes": []
    }
  ]
}
```
A report states the query that was send, an array of inserted objects and an array of deleted objects: Inserted or deleted objects represent a single triple with s, p and o being subject, predicate and object.

## Expanding our mail handling microservice
We need to notify the delta service of the existence of our mail handling service. We do this using the subscribers.json file that was created in part 1. Change it so it looks like:
```
{
  "potentials":[
  ],
    "effectives":[
	"http://mailservice/process_delta"
  ]
}
```
In the docker-compose.yml file we need to alter the delta-service definition to look like:
```
  delta:
    image: semtech/mu-delta-service:beta-0.8
    links:
      - db:db
      - mailservice:mailservice
    volumes:
      - ./config/delta-service:/config
    environment:
      CONFIGFILE: "/config/config.properties"
      SUBSCRIBERSFILE: "/config/subscribers.json"
```
That way the delta service can talk to the mailservice.

To handle delta reports in our mail handling microservice we will need 2 things:
* get access to the POST body of a request
* process and manipulate JSON data

To get access to this add the following imports to your web.py file:
```
import json
from flask import request
```

Then we define a new method that will handle the incoming delta reports:
```
@app.route("/process_delta", methods=['POST'])
def processDelta():
```

We load the delta report in to a variable and define some variables. Lastly we define an array that will hold the URI's  of all emails that need to be send.

```
delta_report = json.loads(request.data)
mails_to_send = set()
predicate_mail_is_ready = "http://example.com/ready"
value_mail_is_ready = "yes"
```

We will loop over all inserted triples to check for mails that are ready to be send:
```
    for delta in delta_report['delta']:
        for triple in delta['inserts']:
            if(triple['p']['value'] == predicate_mail_is_ready):
                if(triple['o']['value'] == value_mail_is_ready):
                    mails_to_send.add(triple['s']['value'])
```
After this for loop has run all the URI's of mails that are ready to be send ill be in the mails_to_send array.
Now we loop over the array and query the database for each URI in the set. And then we will fetch a mail object
for every URI that is in the set.

Add the next code to the mail_helpers.py file:
```
    # this query will find the mail (if it exists)
    select_query = "SELECT DISTINCT ?uuid ?from ?ready ?subject ?content\n"
    select_query += "WHERE \n{\n"
    select_query += "<" + str(uri) + "> <http://mail.com/from> ?from;\n"
    select_query += "a <http://mail.com/Mail>;\n"
    select_query += "<http://mail.com/content> ?content;\n"
    select_query += "<http://mail.com/subject> ?subject;\n"
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
    mail['sender'] = bindings['from']['value']
    mail['ready'] = bindings['ready']['value']
    mail['subject'] = bindings['subject']['value']
    mail['content'] = bindings['content']['value']
    
    return mail
```
This function load_mail will load the mail object from the triple store. There is still the chance that the
ready predicate was sent for some other object, or for an a mail that does not have all required fields or for
an object that is not a mail but happens to use the same predicate.

We will use this function to try to load a mail object for each URI. Because the query was build without OPTIONAL
statements we are certain that an the dictionary returned by the load_mail function will either have all keys or
none.

To send the mail I have copied the entire send_mail function from http://naelshiab.com/tutorial-send-email-python/ and modified
it slightly to take into account the dictionary object that now describes the mail.
```
def send_mail(mail):
    
    fromaddr = "YOUR EMAIL"
    toaddr = "EMAIL ADDRESS YOU SEND TO"
    
    msg = MIMEMultipart()
    
    msg['From'] = mail['from']
    msg['To'] = mail['to']
    msg['Subject'] = mail['subject']
    
    body = mail['content']
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "YOUR PASSWORD")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
```

The last thing that we need to do is to connect the list of URI's to the send_mail function like:
```
    for uri in mails_to_send:
        mail = mail_helpers.load_mail(uri)
        if 'uuid' in mail.keys():
            mail_helpers.send_mail(mail, EMAIL_ADDRESS, EMAIL_PWD)
```

To test this you can send a POST request similar to this one to your local mu.semte.ch application on http://localhost/mails:
```
{"data":{
  "attributes":{
	"from":"flowofcontrol@gmail.com",
	"subject":"A mail from the triple store",
	"content":"This mail was sent by a micro service that listens to your triple store.",
	"ready":"yes",
	"to":"flowofcontrol@gmail.com"
	},
 "type":"mails"
 }}
 ```
 If all went well then the person whose email address you filled in in the from field will have gotten a mail from you.
 