#!/usr/bin/python

# Start by importing the libraries we want to use

import RPi.GPIO as GPIO # This is the GPIO library we need to use the GPIO pins on the Raspberry Pi
import smtplib # This is the SMTP library we need to send the email notification
import time # This is the time library, we need this so we can use the sleep function

# Define some variables to be used later on in our script

# You might not need the username and password variable, depends if you are using a provider or if you have your raspberry pi setup to send emails
# If you have setup your raspberry pi to send emails, then you will probably want to use 'localhost' for your smtp_host

smtp_username = "enter_username_here" # This is the username used to login to your SMTP provider
smtp_password = "enter_password_here" # This is the password used to login to your SMTP provider
smtp_host = "enter_host_here" # This is the host of the SMTP provider
smtp_port = 25 # This is the port that your SMTP provider uses

smtp_sender = "sender@email.com" # This is the FROM email address
smtp_receivers = ['receiver@email.com'] # This is the TO email address

# The next two variables use triple quotes, these allow us to preserve the line breaks in the string. 

# This is the message that will be sent when NO moisture is detected

message_dead = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification

Warning, no moisture detected! Plant death imminent!!! :'(
"""

# This is the message that will be sent when moisture IS detected again

message_alive = """From: Sender Name <sender@email.com>
To: Receiver Name <receiver@email.com>
Subject: Moisture Sensor Notification

Panic over! Plant has water again :)
"""

# This is our sendEmail function

def sendEmail(smtp_message):
	try:
		smtpObj = smtplib.SMTP(smtp_host, smtp_port)
		smtpObj.login(smtp_username, smtp_password) # If you don't need to login to your smtp provider, simply remove this line
		smtpObj.sendmail(smtp_sender, smtp_receivers, smtp_message)         
		print "Successfully sent email"
	except SMTPException:
		print "Error: unable to send email"

# This is our callback function, this function will be called every time there is a change on the specified GPIO channel, in this example we are using 17

def callback(channel):  
	if GPIO.input(channel):
		print "LED off"
		sendEmail(message_dead)
	else:
		print "LED on"
		sendEmail(message_alive)

# Set our GPIO numbering to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin that we have our digital output from our sensor connected to
channel = 17
# Set the GPIO pin to an input
GPIO.setup(channel, GPIO.IN)

# This line tells our script to keep an eye on our gpio pin and let us know when the pin goes HIGH or LOW
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
# This line asigns a function to the GPIO pin so that when the above line tells us there is a change on the pin, run this function
GPIO.add_event_callback(channel, callback)

# This is an infinte loop to keep our script running
while True:
	# This line simply tells our script to wait 0.1 of a second, this is so the script doesnt hog all of the CPU
	time.sleep(0.1)
