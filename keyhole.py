# Keyhole
# This is a program to securely manage the many passwords I have to remember.
# Where every account I use online needs to have a different password, it's
# nearly impossible to remember them all. It almost seems like the password
# recovery function of a website ends up being my password solution. I think
# that's kind of silly. This is a program that will help me remedy this.

import getpass
import os.path
import mmap
import sys
import random
import time
import json
import bcrypt
#import pyAesCrypt
#import io
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
DATA_FILE = "-data"
LOGIN_FILE = ".login.json"

# program_data maps usernames to dictionaries mapping accounts to encrypted passwords
program_data = {}

# Stores the usernames and encrypted master passwords
login_data = {}

master_pass = ""


def hash_password(password):
    # Add a cost factor by slowing down the hashing. This increases security.
    salt = bcrypt.gensalt(rounds=16)
    # Pass the byte representation of the password
    hashed_pass = bcrypt.hashpw(password.encode(), salt)
    return str(hashed_pass)

def prompt_password(new=False):
    password = ""
    conf_pass = ""

    if new == True:
        while True:
            password = getpass.getpass(prompt='Enter a new password: ', stream=None)
            conf_pass = getpass.getpass(prompt='Confirm password: ', stream=None)
            print("")
            if len(password) > 0 and password == conf_pass:
                break
            else:
                print("The passwords didn't match...")
                print("")
        return password
    else:
        password = getpass.getpass()
        hashed_pass = hash_password(password)
        if bcrypt.checkpw(password, hashed_pass.encode()) != True:
            print("Invalid password.")
            exit()
        print("")
        return password

def create_user(username=""):
    global login_data 
    global master_pass

    do_create = input("Username doesn't exist. Create one? [Y/n] ")
    if do_create == 'Y' or do_create == 'y':
        ans = input(f"Is the name '{username}' okay? [Y/n] ")
        if ans == 'n' or ans == 'N':
            valid = 0
            while valid == 0:
                username = input("Enter a new username: ")
                # Check if user exists
                if key in login_data.keys():
                    print("That username already exists.")
                else:
                    valid = 1
    else:
        print("Exiting...")
        exit()

    password = prompt_password(new=True)
    master_pass = password
    hashed_pass = hash_password(password)
    # The salt needs to be stored for encrypting and decrypting program data with Fernet 
    salt = os.urandom(16)
    
    # Add the new user to the dictionary mapping it to the hashed password and the salt
    # that will be used later for decrypting the data.
    # This puts the salt in a different file than the encrypted program data
    login_data[username] = [hashed_pass, salt]
    print(f"Hashed pass to be saved: {hashed_pass}")
    # Save the password to the file to be encrypted as well 
    #program_data[username] = {"this_program": password} 
    return username

def prompt_credentials():
    global login_data 
    name = input("Username: ")
    if len(name) == 0:
        print("Invalid username.")
        exit()
    if name in login_data.keys():
        master_pass = prompt_password() 
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
    print("Success so far!")


def add_account(username):
    global program_data
    print("")
    account = input("Enter the name of the account: ")
    password = prompt_password(new=True)
    program_data[username][account] = password # TODO: Needs to be encrypted 
    print("Account added!")
    print("")

def update_account_pass(username):
    global program_data
    prompt = "Enter the number of the account for the password you'd like to update: "  
    selection = select_account_with_prompt(username, prompt)
    new_pass = prompt_password(new=True)
    accounts = list(program_data[username])
    program_data[username][accounts[selection]] = new_pass 
    print("Password updated!")
    print("")

def remove_account(username):
    global program_data
    prompt = "Enter the number of the account you'd like to delete: "   
    selection = select_account_with_prompt(username, prompt) 
    accounts = list(program_data[username])
    del program_data[username][accounts[selection]]
    print("Account removed!")
    print("")

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
    print("\t4) Remove account and password?")
    print("\t5) Exit")
    print("")

    selection = ""
    invalid = True
    while invalid:
        selection = input("Enter the number of your selection: ")
        if selection.isdigit() == False:
            print("Invalid selection.")
        elif int(selection) < 1 or int(selection) > num_options:
            print("Invalid selection.")
        else:
            invalid = False
    return int(selection)

def do_action(action, username):
    global program_data
    if action == 1:
        # View an account password
        view_account_pass(username)
    elif action == 2:
        # Add a new account and password
        add_account(username)
        pass
    elif action == 3:
        # Update an account's password
        update_account_pass(username) 
        pass
    elif action == 4:
        # Remove an account and password
        remove_account(username)
        pass
    else: 
        return False
    return True



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
       time.sleep(1/(i+2))
    
       # Clear the line in the terminal
       sys.stdout.write("\033[K")

def load_login_data():
    global login_data

    # This will load the login file or any backups if something when wrong
    if os.path.exists(LOGIN_FILE):
        with open(LOGIN_FILE) as json_login_file:
            login_data = json.load(json_login_file)
    elif os.path.exists(LOGIN_FILE + ".new"):
        with open(LOGIN_FILE + ".new") as json_login_file:
            login_data = json.load(json_login_file)
    elif os.path.exists(LOGIN_FILE + ".bak"):
        with open(LOGIN_FILE + ".bak") as json_login_file:
            login_data = json.load(json_login_file)




# Load the json data file and place it in the program_data dictionary 
def load_data(username):
    global program_data
    
    program_data_json = ""

    cipher = Fernet(derive_key(username))

    if os.path.exists("." + username + DATA_FILE):
        with open("." + username + DATA_FILE, "rb") as encrypted_data_file:
            encrypted_json = encrypted_data_file.read()
            decrypted_json = cipher.decrypt(encrypted_json)
            program_data = json.loads(decrypted_json)

    ## Decryption buffer size
    #buffer_size = 500 * 1024 
    ##f_ciph = io.BytesIO()
    #f_dec = io.BytesIO()

    ## Read the encrypted file
    ## Decrypt it
    ## Deserialize the json and place it in program_data

    ## TODO: Problem: Somehow I'm corrupting the file either when writing it or reading it. 
    #if os.path.exists(DATA_FILE):
    #    with open(DATA_FILE, "rb") as encrypted_data_file:
    #        encrypted_text = encrypted_data_file.read()
    #        print(f"Raw text first: {encrypted_text}")
    #        ctlen = sys.getsizeof(encrypted_text)
    #        f_ciph = io.BytesIO(encrypted_text)
    #        #f_ciph = io.BytesIO(b"stuff")
    #        print(f"Ciphertext: {str(f_ciph.getvalue())}")
    #        f_ciph.seek(0)
    #        pyAesCrypt.decryptStream(f_ciph, f_dec, master_pass, buffer_size, ctlen)
    #        program_data_json = str(f_dec.getvalue())
    #        program_data = json.loads(program_data_json)

    ## Load the encrypted file
    #if os.path.exists(DATA_FILE):
    #    with open(DATA_FILE) as encrypted_data_file:
    #        
    #        program_data = json.load(json_data_file)
    #elif os.path.exists(DATA_FILE + ".new"):
    #    with open(DATA_FILE + ".new") as json_data_file:
    #        program_data = json.load(json_data_file)
    #elif os.path.exists(DATA_FILE + ".bak"):
    #    with open(DATA_FILE + ".bak") as json_data_file:
    #        program_data = json.load(json_data_file)


def derive_key(username):
    # The password has to be run through a key derivation function 
    # in order to be used with Fernet
    kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=login_data[username][1], # The salt is stored here
            iterations=100000,
            backend=default_backend()
            )
    key = base64.urlsafe_b64encode(kdf.derive(master_pass.encode())) 
    return key


def save_data(username):
    global program_data
    global login_data

    # Convert the program_data to json
    prog_content = json.dumps(program_data)
   
    print("SAVING DATA")
    
    # Encrypt the prog_content json string
    key = derive_key(username) 
    f = Fernet(key)    
    encrypted_data = f.encrypt(prog_content.encode())

    # Carefully overwrite the old data. This is so it can be preserved if
    # the program closes before saved.
    
    # Program Data
    # Write the new data to a .new file to preserve the old 
    
    # Encryption/decription buffer size in bytes
   # buffer_size = 500 * 1024 # TODO: Set this more intelligently...

    # Input plaintext binary stream
   # f_in = io.BytesIO(prog_content.encode())
    
    # Initialize ciphertext binary stream
   # f_ciph = io.BytesIO()

    # Encrypt stream
   # pyAesCrypt.encryptStream(f_in, f_ciph, master_pass, buffer_size)
   
    # TODO: Somehow I'm corrupting the file either here or when I load it.
    # Write the encrypted data to the file
    f = open("." + username + DATA_FILE, "wb")
    #f.write(str(f_ciph.getvalue()))   
    #f.write(f_ciph.getvalue())   
    f.write(encrypted_data)

    # Login Data
    # Convert the login data to json
    print("About to json dump!")
    
    #with open(LOGIN_FILE + ".new", "w") as fp: 
    #    json.dump(login_data, fp)
    #print("Did it!")
  
    # TODO: Because the hash is stored as bytes, json can't serialize it.
    # Maybe I could work around this somehow
    login_conent = json.dumps(login_data)


    # Write the new data to a .new file to preserve the old 
    f = open(LOGIN_FILE + ".new", "w")
    f.write(login_content)   

    # Rename the old file as a backup
    #if os.path.exists(LOGIN_FILE):
    #    os.rename(LOGIN_FILE, LOGIN_FILE + ".bak")

    # Make the .new file as the new base
    #os.rename(LOGIN_FILE + ".new", LOGIN_FILE)

    # Remove the backup
    #if os.path.exists(LOGIN_FILE + ".bak"):
    #    os.remove(LOGIN_FILE + ".bak")



# Display password accounts
# Prompt user for which one to return the password for
# TODO: I need to have a timeout if there isn't user input for a bit
def main():
    # The saved program data file will be loaded into this on startup as well.
    load_login_data() 
    username = prompt_credentials()
    load_data(username)

    # Update the program data for new users. Nothing will change
    # for an existing user
    # If this is the first user.
    if len(list(program_data)) == 0:
        program_data[username] = {"this_program": master_pass} 
    # If not the first user, but is a new user 
    elif key not in program_data.keys():
        program_data[username] = {"this_program": master_pass}
    
    print(f"Welcome, {username}.") 

    repeat = True
    while repeat:
        print("********************************************************")
        action = get_action(username)

        # Perform the action
        repeat = do_action(action, username)
        save_data(username)

    print("")
    print("Locking up...")
    print("Until next time!")

if __name__ == '__main__':
    main()


# I need to generate a random salt, add it to the password, and hash it.
# The hashed password + salt is what I need to store along with the salt.
# I could store this like salt:hasedPasswordPlusSalt

# When logging in, I need to grab the stored salt for that username,
# add it to the inputted password, hash it, and see if it matches the stored
# hash. If so, access can be granted.

# How do I generate the random salt?
# What should I use for the hasing? bcrypt?

# The next question is how do I secure all of the other passwords that are
# stored for each user? A hash isn't something that can be undone. It can just
# take something, hash it, and then see if the hash matches what's stored.
# In this program, however, I need to be able to undo however the other 
# passwords are stored. How do I do that securely?

# I think I need a file for usernames and master passwords.
# I think I need a separate file for all accounts and passwords for each user.
# Logging in will use the first password. If it checks out, I can use that
# inputted password as the key to unencrypt the accounts/passwords file.






