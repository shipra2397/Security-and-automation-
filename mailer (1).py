import smtplib
import datetime
import time
from datetime import datetime
import config
import traceback
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders

# Set now to whatever time it currently is
now = datetime.now()

def email(filename):
	# Define the email subject
	SUBJECT = "Someone is at the door " + time.strftime('%Y')
	# Create a variable based on the configuration recipient
	RECIPIENT_EMAIL = config.RECIPIENT_EMAIL
	# If the recipient field is blank in the config the email should go to the sender
	if (RECIPIENT_EMAIL == ''):
		RECIPIENT_EMAIL = config.SENDER_EMAIL
	# Create the email
	msg = MIMEMultipart()
	msg['Subject'] = SUBJECT 
	msg['From'] = config.SENDER_EMAIL
	msg['To'] = RECIPIENT_EMAIL
	part = MIMEBase('application', "octet-stream")
	part.set_payload(open(filename, "rb").read())
	Encoders.encode_base64(part)
	part.add_header('Content-Disposition', 'attachment; filename="'+filename+'"')
	msg.attach(part)
	# Connect to the email server
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.ehlo()
	server.starttls()
	# Log into the sender email address and send the email
	try:
		server.login(config.SENDER_EMAIL, config.SENDER_PASSWORD)
		server.sendmail(config.SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
		print "Email Sent!"
	except Exception:
		print('Login Failed!')
		print(traceback.format_exc())
	# Close server connection
	server.quit
