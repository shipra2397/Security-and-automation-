import io
import imaplib
import email
import RPi.GPIO as GPIO
import cv2
import os
import config
import face
import hardware
import mailer
import time
from datetime import datetime


if __name__ == '__main__':
	# Load training data into model
	print 'Loading training data...'
	model = cv2.face.EigenFaceRecognizer_create()
	model.read(config.TRAINING_FILE)
	print 'Training data loaded!'
	# Initialize camer and box.
	camera = config.get_camera()
	print 'Running box...'
	print 'Press button to lock (if unlocked), or unlock if the correct face is detected.'
	print 'Press Ctrl-C to quit.'
	while True:
                                emailSent= False
				print 'Button pressed, looking for face...'
				# Check for the positive face and unlock if found.
				image = camera.read()
				# Convert image to grayscale.
				image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
				# Get coordinates of single face in captured image.
				result = face.detect_single(image)
				if result is None:
					print 'Could not detect single face!  Check the image in capture.pgm' \
						  ' to see what was captured and try again with only one face visible.'
					continue
				x, y, w, h = result
				# Crop and resize image to face.
				crop = face.resize(face.crop(image, x, y, w, h))
				
				put=cv2.equalizeHist(crop)
				# Test face against model.
				label, confidence = model.predict(put)
				print 'Predicted {0} face with confidence {1} (lower is more confident).'.format(
					'POSITIVE' if label == config.POSITIVE_LABEL else 'NEGATIVE', 
					confidence)
				if confidence < config.POSITIVE_THRESHOLD:
					print 'Recognized face!'
					GPIO.setmode(GPIO.BOARD)
                                        GPIO.setup(11,GPIO.OUT)
                                        GPIO.output(11,1)
                                        print 'Led On!!!!!!!!!'
				else:
					print 'Did not recognize face!'
					# Someone other than the box owner is trying to get in. Save a picture of their face...
					if(not emailSent):
						# Only send an email if the user has email information stored
						if (not config.SENDER_EMAIL == ''):
                                                        filename = os.path.join('./culprits/',time.strftime('%Y')+ '_face.png')
							cv2.imwrite(filename, crop)
							mailer.email(filename)
							emailSent = True

							os.system("raspivid -o - -t 0 -hf -w 800 -h 400 -fps 24 |cvlc -vvv stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst=:8000}' :demux=h264")



							
							mail = imaplib.IMAP4_SSL('imap.gmail.com')
                                                        mail.login('sarthakk66@gmail.com', '1Sarthakkapoor')
                                                        mail.list()
                                                        # Out: list of "folders" aka labels in gmail.
                                                        mail.select("inbox") # connect to inbox.
                                                        result, data = mail.search(None, "ALL")

                                                        ids = data[0] # data is a list.
                                                        id_list = ids.split() # ids is a space separated string
                                                        first_email_id = int(id_list[0])
                                                        latest_email_id = id_list[-1] # get the latest

                                                        # fetch the email body (RFC822) for the given ID
                                                        result, data = mail.fetch(latest_email_id, "(RFC822)") 

                                                        raw_email = data[0][1] # here's the body, which is raw text of the whole email
                                                        # including headers and alternate payloads
                                                        for response_part in data:
                                                            if isinstance(response_part, tuple):
                                                                msg = email.message_from_string(response_part[1])
                                                                email_subject = msg['subject']
                                                                email_from = msg['from']
                                                                print msg
                                                                print 'From : ' + email_from + '\n'
                                                                print 'Subject : ' + email_subject + '\n'
                                                                if (email_subject=='1'):
                                                                    GPIO.setmode(GPIO.BOARD)
                                                                    GPIO.setup(11,GPIO.OUT)
                                                                    GPIO.output(11,1)
                                                                    print('ma chuda')

                                                        

 					
