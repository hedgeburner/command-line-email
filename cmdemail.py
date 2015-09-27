#!/usr/bin/env python3
#coded for python 3.3+

import sys, os
import argparse, smtplib
import shelve, getpass
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
        self.__dict__.update(kwds)  
        self.name = str(name)
        
    @classmethod
    def load_user(cls, command_args, datafile='userdata'):
        """load a user from the prepared command line args and the database."""
        user = command_args.pop('user')
        try:
            with shelve.open(datafile) as file:
                command_args.update(file[user])
        except KeyError:
            new = create_new_user(user, datafile)
            command_args.update(new)
        if command_args['subject'] is None:
            command_args['subject'] = command_args['default_subject']
        return cls(user, **command_args)
        
    @property
    def password(self):
        return getpass.getpass('Email password: ')

    
def get_user():
    """
    identify the user of the current process.
    """
    return getpass.getuser()
    
def create_new_user(username, datafile):
    """create a new user, store it in datafile. return user data as dict."""
    print('Hello, you are new to this program.')
    address = input("Your Email address: ")
    smtp = input('Address of your smtp server: ')
    subject = input("If you don't type in a subject line, what should be used as a default? ")
    data = {'email': address,
            'host': smtp,
            'default_subject': subject}
    print("saving your data...")
    with shelve.open(datafile) as file:
        file[username] = data
    return data
        
def email_from_text(text, subject=''):
    """create a message object from a given text."""
    msg = email.message_from_string(text, policy=policy.EmailPolicy())
    msg['Subject'] = subject
    return msg

def send(msg, user):
    msg['From'] = user.email
    msg['To'] = user.address
    
    with smtplib.SMTP(user.host) as smtp:
        smtp.login(user.email, user.password)
        smtp.send_message(msg)
        
def parse_arguments():
    """ parse the command line arguments """
    parser = argparse.ArgumentParser(description='Send an Email from the command line.')
    parser.add_argument('address', help='The Email address of the recipient.')
    parser.add_argument('-s', '--subject', nargs=1, default=None, dest='subject',
                        help='the email subject.')
    parser.add_argument('message', nargs='+', help='The text of the email body.')
    parser.add_argument('-u', '--user', nargs=1, dest='user',
                        help='choose a user name. This defaults to the current user of the console')
    return parser.parse_args()
    
def prepare_arguments(command_args):
    """prepare the command line arguments. return a dict."""
    data = vars(command_args)
    data['user'] = get_user() if (command_args.user is None) else command_args.user[0]
    data['message'] = ' '.join(command_args.message)
    if command_args.subject is not None:
        data['subject'] = command_args.subject[0]
    return data
        
if __name__ == '__main__':
    user = User.load_user(prepare_arguments(parse_arguments()), 'userdata')
    msg = email_from_text(user.message, user.subject)
    send(msg, user)
    print('Email successfully send.')
        

