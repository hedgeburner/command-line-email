#!/usr/bin/env python3
#coded for python 3.3+

import sys, os, pwd
import argparse, smtplib
import email
from email import policy

class User:
    """
    class representing a user. A default user ist selected
    according to who uses the current operating system.
    """
    def __init__(self, name=None, **kwds):
        if name is None:
            name = get_user()
        else:
            self.__dict__.update(kwds)  
        self.name = str(name)
        
    @property
    def password():
        return '*'
    
def get_user():
    """
    identify the user of the current process.
    """
    return pwd.getpwuid(os.getuid())[0]
        
def email_from_text(text, subject=''):
    """create a message object from a given text."""
    msg = email.message_from_string(text, policy=policy.EmailPolicy())
    msg['Subject'] = subject
    return msg
        

