# Keyhole
# This is a program to securely manage the many passwords people have to 
# remember. Where every account online needs to have a different password, it's
# nearly impossible to remember them all. It almost seems like the password
# recovery function of a website ends up being the password solution. This is 
# annoying. This is a program that helps remedy this by securely storing
# them for lookup.
#
# Written by Daniel Hornberger
# 10/18/2019
# Version 0.1.3

import getpass
import os.path
import sys
import signal
import random
import time
import threading
import json
import bcrypt
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

print("")
print("")
print("*******************************************************")
print("* |   /                         _____                 *")
print("* |  /                         /*****\\                *")
print("* | /   x----- \\    / |     | /*******\\ |     x-----  *")
print("* |/    |       \\  /  |     | \\*******/ |     |       *")
print("* |\\    |__      \\/   |_____|  \\*****/  |     |__     *")
print("* | \\   |        ||   |     |   |***|   |     |       *")
print("* |  \\  |        ||   |     |   |***|   |     |       *")
print("* |   \\ x-----   ||   |     |   \\***/   |____ x-----  *")
print("*                                                     *")
print("*******************************************************")
print("")
print("")

# The file containing the saved usernames, accounts, and passwords
DATA_PATH = ".keyhole/"
DATA_FILE = DATA_PATH + ".data-"
LOGIN_FILE = DATA_PATH + ".login.json"

if not os.path.exists(DATA_PATH):
    try:
        os.mkdir(DATA_PATH)
    except OSError:
        print("Failed to create program data directory. Exiting...")
        exit()

# program_data maps usernames to dictionaries mapping accounts to encrypted passwords
program_data = {}

# Stores the usernames and encrypted master passwords
login_data = {}

master_pass = ""

def handle_timeout():
    print("\n\nLocking up due to inactivity...")
    os._exit(os.EX_OK)

# Global timer to close the program if there's no user input for two minutes
timeout_secs = 120
timer = threading.Timer(timeout_secs, handle_timeout)
timer.start()

def signal_handler(sig, frame):
    # Clean up the threads on Ctrl+c 
    timer.cancel()
    quit() 

signal.signal(signal.SIGINT, signal_handler)

# This is used whenever there is user input to restart the timer
def reset_timer():
    global timer
    timer.cancel()
    timer = threading.Timer(timeout_secs, handle_timeout)
    timer.start()

def hash_password(password):
    # Add a cost factor by slowing down the hashing. This increases security.
    salt = bcrypt.gensalt(rounds=16)
    # Pass the byte representation of the password
    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    # For json serialization, it can't be bytes type, so I decode it here
    # The salt will also be used for generating the key to encrypt/decrypt the 
    # program data
    return hashed_pass.decode('utf-8'), salt.decode('utf-8') 

def prompt_password(new=False, username=""):
    password = ""
    conf_pass = ""

    if new == True:
        while True:
            password = getpass.getpass(prompt='Enter a new password: ', stream=None)
            reset_timer()
            conf_pass = getpass.getpass(prompt='Confirm password: ', stream=None)
            reset_timer()
            print("")
            if len(password) > 0 and password == conf_pass:
                break
            else:
                print("The passwords didn't match...")
                print("")
        return password
    else:
        password = getpass.getpass()
        reset_timer()

        # Check if the hash of the inputted password matches the saved hash for the user
        if bcrypt.checkpw(password.encode(), login_data[username][0].encode()) != True:
            print("Invalid password.")
            exit()
        master_pass = password
        print("")
        print("Access granted...")
        print("")
        return password

def create_user(username=""):
    global login_data 
    global master_pass

    do_create = input("Username doesn't exist. Create one? [Y/n] ")
    reset_timer()
    if do_create == 'Y' or do_create == 'y':
        ans = input(f"Is the name '{username}' okay? [Y/n] ")
        reset_timer()
        if ans == 'n' or ans == 'N':
            valid = 0
            while valid == 0:
                username = input("Enter a new username: ")
                reset_timer()
                # Check if user exists
                if username in login_data.keys():
                    print("That username already exists.")
                else:
                    valid = 1
    else:
        print("Exiting...")
        os._exit(os.EX_OK)

    password = prompt_password(new=True)
    master_pass = password
    hashed_pass, salt = hash_password(password)
    
    # Add the new user to the dictionary mapping it to the hashed password and the salt
    # that will be used later for decrypting the data.
    login_data[username] = [hashed_pass, salt] 
    return username

def prompt_credentials():
    global login_data
    global master_pass
    name = input("Username: ")
    reset_timer()

    if len(name) == 0:
        print("Invalid username.")
        exit()
    if name in login_data.keys():
        master_pass = prompt_password(username=name) 
        return name
   
    name = create_user(name)
    return name

def list_accounts(username):
    global program_data
    accounts = list(program_data[username])
    print("")
    for num, acnt in enumerate(accounts):
        print(f"\t{num + 1}) {acnt}") 
    print("")

def select_account_with_prompt(username, prompt):
    global program_data
    list_accounts(username)
    accounts = list(program_data[username])
    num_options = len(accounts) + 1
    selection = ""
    invalid = True
    while invalid:
        selection = input(prompt)
        reset_timer()
        if selection.isdigit() == False:
            print("Invalid selection.")
        elif int(selection) < 1 or int(selection) > num_options:
            print("Invalid selection.")
        else:
            invalid = False
    return int(selection) - 1

def view_account_pass(username):
    global program_data
    prompt = "Enter the number of the account for the password you'd like to see: "
    selection = select_account_with_prompt(username, prompt) 
    accounts = list(program_data[username])
    display_decaying_pass(program_data[username][accounts[selection]]) 

def add_account(username):
    global program_data
    print("")
    account = input("Enter the name of the account: ")
    reset_timer()
    password = prompt_password(new=True)
    program_data[username][account] = password 
    print("Account added!")
    print("")

def update_account_pass(username):
    global program_data
    global login_data
    global master_pass
    prompt = "Enter the number of the account for the password you'd like to update: "  
    acnt_index = select_account_with_prompt(username, prompt)
    new_pass = prompt_password(new=True)
    accounts = list(program_data[username])
    program_data[username][accounts[acnt_index]] = new_pass
    if acnt_index == 0:
        master_pass = new_pass 
        hashed_pass, salt = hash_password(new_pass)
        login_data[username] = [hashed_pass, salt]
        program_data[username]["this_program"] = new_pass
    
    print("Password updated!")
    print("")

def remove_account(username):
    global program_data
    user_account_deleted = False
    prompt = "Enter the number of the account you'd like to delete: "   
    acnt_index = select_account_with_prompt(username, prompt)
    # Delete account in this program
    if acnt_index == 0:
        ans = input("This will delete your account in this program and remove all saved information. Proceed? [Y/n] ")
        reset_timer()
        if ans == "Y" or ans == "y":
            print("Deleting your account and all information associated with it...")
            del program_data[username]
            del login_data[username]
            print("Exiting...")
            user_account_deleted = True
            return user_account_deleted 
        else:
            return user_account_deleted
    accounts = list(program_data[username])
    del program_data[username][accounts[acnt_index]]
    print("Account removed!")
    print("")
    return user_account_deleted

def get_action(username):
    global program_data
    num_options = 5  
   
    print("")
    print("Your accounts:")
    list_accounts(username)

    print("What would you like to do?") 
    print("")
    print("\t1) View the password of an account?")
    print("\t2) Add a new account and password?")
    print("\t3) Update the password of an account?")
    print("\t4) Remove an account and password?")
    print("\t5) Exit")
    print("")

    selection = ""
    invalid = True
    while invalid:
        selection = input("Enter the number of your selection: ")
        reset_timer()
        if selection.isdigit() == False:
            print("Invalid selection.")
        elif int(selection) < 1 or int(selection) > num_options:
            print("Invalid selection.")
        else:
            invalid = False
    return int(selection)

def do_action(action, username):
    global program_data
    repeat = True
    account_deleted = False
    if action == 1:
        # View an account password
        view_account_pass(username)
    elif action == 2:
        # Add a new account and password
        add_account(username)
    elif action == 3:
        # Update an account's password
        update_account_pass(username) 
    elif action == 4:
        # Remove an account and password
        account_deleted = remove_account(username)
    else:
        repeat = False
   
    return repeat, account_deleted

def display_decaying_pass(password):
    # After the password is obtained, show it briefly and cross it out
    print("")
    print("Showing password...") 
    
    print(password, end='\r')
    time.sleep(2)
    
    # Slowly cross out the password
    indices = random.sample(range(len(password)), len(password))
    for i in range(len(password)):
       temp = list(password)
       
       # Replace a random characterh in password with '*' on each iteration 
       for j in range(i+1):
           temp[indices[j]] = '*' # Random decay
           # temp[j] = '*' # Sequential decay
    
       decayed_pass = "".join(temp)
       print(decayed_pass, end='\r')
       time.sleep(1/((i+1)*2))
    
       # Clear the line in the terminal
       sys.stdout.write("\033[K")

def load_login_data():
    global login_data

    # This will load the login file or any backups if something when wrong
    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE) as json_login_file:
            login_data = json.load(json_login_file)

# Load the json data file and place it in the program_data dictionary 
def load_data(username):
    global program_data
    program_data_json = ""

    cipher = Fernet(derive_key(username))

    if os.path.exists(DATA_FILE + username):
        with open(DATA_FILE + username, "rb") as encrypted_data_file:
            encrypted_json = encrypted_data_file.read()
            decrypted_json = cipher.decrypt(encrypted_json)
            program_data = json.loads(decrypted_json)

def derive_key(username):
    # The password has to be run through a key derivation function 
    # in order to be used with Fernet
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=login_data[username][1].encode(), # The salt is stored here
            iterations=100000,
            backend=default_backend()
            )
    key = base64.urlsafe_b64encode(kdf.derive(master_pass.encode())) 
    return key


def save_data(username, delete_account=False):
    global program_data
    global login_data

    if delete_account == False:
        # Convert the program_data to json
        prog_content = json.dumps(program_data)
        # Encrypt the prog_content json string
        key = derive_key(username) 
        f = Fernet(key)    
        encrypted_data = f.encrypt(prog_content.encode())

        # Write the encrypted data to the file
        f = open(DATA_FILE + username, "wb")
        f.write(encrypted_data)
    else:
        if os.path.exists(DATA_FILE + username):
            os.remove(DATA_FILE + username)

    # Login Data
    # Convert the login data to json and write to file
    login_content = json.dumps(login_data)
    f = open(LOGIN_FILE, "w")
    f.write(login_content)   

def main():
    # The saved program data file will be loaded into this on startup as well.
    load_login_data() 
    username = prompt_credentials()
    load_data(username)
   
    # This is so if the only action done is "Exit" their username will be saved.
    save_data(username)

    # Update the program data for new users. Nothing will change
    if len(list(program_data)) == 0:
        program_data[username] = {"this_program": master_pass} 
    # If not the first user, but is a new user 
    elif username not in program_data.keys():
        program_data[username] = {"this_program": master_pass}
    
    print(f"Welcome, {username}.") 

    repeat = True
    delete_account = False
    while repeat == True and delete_account == False:
        print("********************************************************")
        action = get_action(username)

        # Perform the action
        repeat, delete_account = do_action(action, username)
        save_data(username, delete_account=delete_account)
    
    print("")
    print("Locking up...")
    timer.cancel()

if __name__ == '__main__':
    main()

