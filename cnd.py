#!/usr/bin/env python

import subprocess
import getpass
import socket
import os
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

# Lookup the abuse reporting email for that IP using whois
def whois_lookup(ip):
    command = 'whois %s' % ip
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    cmd_output = process.communicate()

    for item in cmd_output[0].split('\n'):
        if 'OrgAbuseEmail' in item:
            abuse_email = item.strip().split()
            return abuse_email[1]

'''
# Monitor SSH for brute force attempts, pass offenders to whois_lookup()
def ssh_monitor():
    if os.path.isfile("/var/log/auth.log"):
        authlog_f = file("/var/log/auth.log", "r")
'''
 
                
def ip_check(ip):            
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def send_email(abuse_email, sender_email, subject, body, password):
    message = MIMEMultipart()
    message['from'] = sender_email
    message['to'] = abuse_email
    message['subject'] = subject
    message.attach(MIMEText(body))
    
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, sender_email, message.as_string())
    server.quit()


def main():
    if ip_check(sys.argv[1]) == False:
        print "[+] Error: Bad IP address, exiting..."
        exit()
    print '[+] Sending to whois'
    abuse_email = whois_lookup(sys.argv[1])
    password = getpass.getpass()
    sender_email = raw_input("Sender email: ")

    #subject and body are going to be assigned by log parsing
    send_email(abuse_email, sender_email, subject, body, password)


# parse logs to get all abuse IP then sendmail it up

if __name__ == '__main__':
    main()
