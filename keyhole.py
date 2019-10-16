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
DATA_FILE = ".data.json"
# program_data maps usernames to dictionaries mapping accounts to encrypted passwords
program_data = {}

def prompt_password(new=False):
    password_1 = ""
    password_2 = ""

    if new == True:
        while True:
            password_1 = getpass.getpass(prompt='Enter a new password: ', stream=None)
            password_2 = getpass.getpass(prompt='Confirm password: ', stream=None)
            print("")
            if len(password_1) > 0 and password_1 == password_2:
                break
            else:
                print("The passwords didn't match...")
                print("")
        return password_1
    else:
        password_1 = getpass.getpass()
        print("")
        return password_1

def create_user(username=""):
    global program_data 
    do_create = input("Username doesn't exist. Create one? [Y/n] ")
    if do_create == 'Y' or do_create == 'y':
        ans = input(f"Is the name '{username}' okay? [Y/n] ")
        if ans == 'n' or ans == 'N':
            valid = 0
            while valid == 0:
                username = input("Enter a new username: ")
                # Check if user exists
                if key in program_data.keys():
                    print("That username already exists.")
                else:
                    valid = 1
    else:
        print("Exiting...")
        exit()

    password = prompt_password(new=True)

    # Add the new user to the dictionary mapping it to an empty dictionary
    program_data[username] = {"this_program": password} # TODO: This needs to be encrypted
    return username

def prompt_credentials():
    global program_data 
    name = input("Username: ")
    if len(name) == 0:
        print("Invalid username.")
        exit()
    if name in program_data.keys():
        prompt_password() # TODO I need to see if the password checks out
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


# Load the json data file and place it in the program_data dictionary 
def load_data():
    global program_data

    # This will load the file or any backups if something when wrong
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as json_DATA_FILE:
            program_data = json.load(json_DATA_FILE)
    elif os.path.exists(DATA_FILE + ".new"):
        with open(DATA_FILE + ".new") as json_DATA_FILE:
            program_data = json.load(json_DATA_FILE)
    elif os.path.exists(DATA_FILE + ".bak"):
        with open(DATA_FILE + ".bak") as json_DATA_FILE:
            program_data = json.load(json_DATA_FILE)

def save_data():
    global program_data
    # Convert the program_data to json
    content = json.dumps(program_data)

    # Carefully overwrite the old data. This is so it can be preserved if
    # the program closes before saved.

    # Write the new data to a .new file to preserve the old 
    f = open(DATA_FILE + ".new", "w")
    f.write(content)   

    # Rename the old file as a backup
    if os.path.exists(DATA_FILE):
        os.rename(DATA_FILE, DATA_FILE + ".bak")

    # Make the .new file as the new base
    os.rename(DATA_FILE + ".new", DATA_FILE)

    # Remove the backup
    if os.path.exists(DATA_FILE + ".bak"):
        os.remove(DATA_FILE + ".bak")


# Display password accounts
# Prompt user for which one to return the password for
# TODO: I need to have a timeout if there isn't user input for a bit
def main():
    # The saved program data file will be loaded into this on startup as well.
    load_data() 
    username = prompt_credentials()
    print(f"Welcome, {username}.")  

    repeat = True
    while repeat:
        print("********************************************************")
        action = get_action(username)

        # Perform the action
        repeat = do_action(action, username)
        save_data()

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
