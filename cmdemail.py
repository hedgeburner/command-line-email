#!/usr/bin/env python3
#coded for python 3.3+

import sys, os
import argparse, smtplib
import hashlib, shelve, getpass
import email
from email import policy

import Crypto.Cipher as cipher

class User:
    """
    class representing a user. A default user ist selected
    according to who uses the current operating system.
    """
    def __init__(self, name=None, **kwds):
        if name is None:
            name = get_user()
        self.__dict__.update(kwds)  
        self.name = str(name)
        
    @property
    def password(self):
        return getpass.getpass('Email password: ')
    
def get_user():
    """
    identify the user of the current process.
    """
    return getpass.getuser()
    
def retrieve_email_passwd(user, key):
    with shelve.open('userdata') as data:
        blowfish = cipher.Blowfish.new(key)
        passwd = blowfish.decrypt(data[user.name][password])
    return passwd
        
def email_from_text(text, subject=''):
    """create a message object from a given text."""
    msg = email.message_from_string(text, policy=policy.EmailPolicy())
    msg['Subject'] = subject
    return msg

def send(msg, target, host, user):
    msg['From'] = user.address
    msg['To'] = target
    
    with smtplib.SMTP(host) as smtp:
        smtp.login(user.address, user.password)
        smtp.send_message(msg)
        
if __name__ == '__main__':
    address = input("Your Email address: ")
    user = User(address=address)
    mailaddress = input('Your target address: ')
    msg = email_from_text("Hello, World!", "a test")
    hostname = input("Adress of your smtp server: ")
    send(msg, mailaddress, hostname, user)
        

