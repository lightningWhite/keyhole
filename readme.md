# Keyhole

This is a program to securely manage the many passwords people have to
remember. Where every account online needs to have a different password,
it's nearly impossible to remember them all. It almost seems like the password
recovery function of a website ends up being the password solution. This is
annoying. This is a program that helps remedy this by securely storing them
for lookup. This is a command line application.

## Using Keyhole

Keyhole can be used as a raw python application or as a containerized 
application. To run the raw python application, just run `python keyhole.py`.
This, of course, is after installing the dependencies listed below.

To run the containerized application, first build the container in the cloned
directory:
* ./build.sh
* Alternatively:
  * `docker build . -t keyhole:0.1.3`

Once the container is built, it can be run with the following command:
* ./keyhole.sh
* Alternatively:
  * `docker run --rm -ti -v keyhole_vol:/usr/src/app/.keyhole/ keyhole:0.1.3`

This will mount a volume so the data can be persisted.

A simple bash script is provided that runs this Docker command for ease of use.
After cloning, it may be necessary to add executable privileges to it:
`chmod +x keyhole.sh`.

This script could also be copied to `/bin/` and renamed to `keyhole`. This 
would allow the command `keyhole` to be run in any terminal as if it was
a native linux command. Sudo privileges are needed to do this. Note that
either Docker or Podman must be installed for this script to work. Without
Docker or Python, the raw python script must be used with its dependencies
installed.

The installation (copying the script to /bin) can be performed by running
the following:
* ./install.sh

## Features

* Multiple user logins
* Main user login password is hashed
* Accounts and passwords can be added, removed, and updated
* Stored accounts and passwords (including the password for the program)
are encrypted using the user's primary password.
* Once logged in, passwords of accounts can be displayed for two seconds. 
Once the two seconds have passed, the password decays on the screen until
it is overwritten.
* A script to backup the encrypted password file so it can be placed in another
  directory
* A script to restore a backup file to the container volume

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

## TODOs

* The `keyhole` application currently doesn't handle signals correctly. When
  attempting to stop the application by running `docker stop ...`, it gets
  force killed after 10 seconds. This should be fixed.
