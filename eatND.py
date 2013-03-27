"""
Taylor Seale
eatND
March 27, 2013
Pick your favorite food at the Dining Hall!
"""
from parse_rest.connection import register
from parse_rest.datatypes import Object
import smtplib
from email.mime.text import MIMEText
# register the program with parse database
register("NsQ7yd5aoQX35SMBmUjVwFA6rUjctED5CrjH1VcI","9uIgnDxZPMQD2skEqVXFXrGf2K8YBPtT9o8ECgbO")

# declare classes for parse tables
class Menu(Object): # daily menu
	pass

emailText=""
favorites = ["sdh fajita bar","biscuits"]
menu = Menu.Query.all()
items = [i for i in menu]
for i in items:
	for f in favorites:
		if f.lower()==i.item.strip().lower():
			emailText+="They are serving "+f.lower()+" at SDH today!\n"

message = MIMEText(emailText)
message['Subject'] = "eatND"
message['From'] = "tseale@nd.edu"
message['To'] = "tseale@nd.edu"

server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login([username], [password])
server.sendmail("eatND","tseale@nd.edu",message.as_string())
server.quit()

