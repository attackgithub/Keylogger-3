# Keylogger
A simple keylogger that uses Gmail as C&C.

**NOTICE:** DO NOT USE YOUR PERSONAL EMAIL

### Use cases
1. When you want to know what your uncle was using your laptop for

### Install
```pip install -r requirements.txt```

### Commands
1. REMOVE - To remove the keylogger from target
2. PERSIST - To add persistence to the keylogger(Only when -ap option wasn't used)

### Command
1. Login into same Gmail account that the program is using
2. Press Compose, to create a new email
3. Set the "To" field to the email address the program is using
4. Set the "Subject" field to Command
5. In the body field type a command. Right now a command is either REMOVE or PERSIST
6. Press Send and wait, the program only checks for commands every 2 minutes
10. You're basically login into the same email as the program and sending an email to yourself.

### Usage
1. Enable [less-secure-apps](https://myaccount.google.com/lesssecureapps) on your gmail(DO NOT USE YOUR PERSONAL EMAIL)
2. Change directory to the build folder
3. run python build.py -h
4. Use "-t python" option to create a normal Python File
5. Use "-t exe" option to create an executable(Only on Windows)


### Video
Watch it [here](https://www.youtube.com/watch?v=vBwotqamsxg)
