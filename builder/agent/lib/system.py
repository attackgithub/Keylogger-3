# Date: 01/28/2019
# Author: Mohamed
# Description: System info

import socket
import geocoder
from getpass import getuser
from platform import system, release


class System:

    def __init__(self):
        self.username = getuser()
        self.external_ip = geocoder.ip('me').ip 
        self.internal_ip = self.get_interal_ip()
        self.version = '{} {}'.format(system(), release())
    
    def get_interal_ip(self):
        ip = ''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
            s.close()
        except:
            pass
        return ip