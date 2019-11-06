# Keyhole

This is a program to securely manage the many passwords people have to
remember. Where every account online needs to have a different password,
it's nearly impossible to remember them all. It almost seems like the password
recovery function of a website ends up being the password solution. This is
annoying. This is a program that helps remedy this by securely storing them
for lookup. This is a command line application.

## Features

* Multiple user logins
* Main user login password is hashed
* Accounts and passwords can be added, removed, and updated
* Stored accounts and passwords (including the password for the program)
are encrypted using the user's primary password.
* Once logged in, passwords of accounts can be displayed for two seconds. 
Once the two seconds have passed, the password decays on the screen until
it is overwritten.


## Security Features 

* `getpass` is used when users input passwords. This makes it so the password
is not shown on the screen as it is being typed.
* The user's primary password is hashed with a salt and saved in the 
`.login_json` file. When the salt is generated, 16 rounds are used so it takes
several seconds to hash the password.
* The accounts and associated passwords entered, including the primary password,
are encrypted using the primary password. Note that if the primary password is
lost or forgotten, there is no recovery method for that user's data. It can only
be decrypted using the primary password. This is either a feature or missing
functionality - however you want to look at it.
* Unencrypted passwords are never written to disk. This data is only ever 
unecrypted when it's in memory while running the program.
* The Bcrypt and Cryptography libraries were used for hashing and encryption.

## Disclaimers

Although, every effort was exerted to make this application secure, no
application is ever perfectly flawless. There are a few areas of possible
concern to highlight:

* Although the primary password is hashed for logging into the program,
that same password is just encrypted in the user's .data file. Encryption
is not a failsafe mechanism for storing passwords. However, this enrypted
data can only be uncrypted with the user's hashed password and the same
salt used for hashing it.
* The usernames are not encrypted. Anyone can see the username associated
with the program.

Use this program at your own risk. It is provided "as is" and no one 
is responsible or liable for anything that adversely arises from its use.

This is not yet licensed.

## Project Setup
Setup a virtual environment: 
* Install python3-venv package: `sudo apt install python3-venv`
* Setup python virtual environment: `python -m venv keyhole`
* Activate virtual environment: source keyhole/bin/activate

### Dependencies
Make sure the dependencies of bcrypt are installed: 
`sudo apt-get install build-essential libffi-dev python-dev`

Install bcrypt: `pip3 install bcrypt`
Install cryptography: `pip3 install cryptography`

