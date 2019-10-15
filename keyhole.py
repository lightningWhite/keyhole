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
print("********************************************************")
print("* |   /                         _____                  *")
print("* |  /                         /*****\\                 *")
print("* | /   x----- \\    / |     | /*******\\ |     x-----   *")
print("* |/    |       \\  /  |     | \\*******/ |     |        *")
print("* |\\    |__      \\/   |_____|  \\*****/  |     |__      *")
print("* | \\   |        ||   |     |   |***|   |     |        *")
print("* |  \\  |        ||   |     |   |***|   |     |        *")
print("* |   \\ x-----   ||   |     |   \\***/   |____ x-----   *")
print("********************************************************")
print("")
print("")

# The file containing the saved usernames, accounts, and passwords
data_file = ".data.json"

def prompt_password():
    password = getpass.getpass()
    return password

def create_user(program_data, username=""):
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

    # Add the new user to the dictionary mapping it to an empty dictionary
    program_data[username] = {}
    return username

# Load the json data file and place it in the program_data dictionary 
def load_data():
    program_data = {}

    # This will load the file or any backups if something when wrong
    if os.path.exists(data_file):
        with open(data_file) as json_data_file:
            program_data = json.load(json_data_file)
    elif os.path.exists(data_file + ".new"):
        with open(data_file + ".new") as json_data_file:
            program_data = json.load(json_data_file)
    elif os.path.exists(data_file + ".bak"):
        with open(data_file + ".bak") as json_data_file:
            program_data = json.load(json_data_file)
    return program_data

def save_data(program_data):
    # Convert the program_data to json
    content = json.dumps(program_data)

    # Carefully overwrite the old data. This is so it can be preserved if
    # the program closes before saved.

    # Write the new data to a .new file to preserve the old 
    f = open(data_file + ".new", "w")
    f.write(content)   

    # Rename the old file as a backup
    if os.path.exists(data_file):
        os.rename(data_file, data_file + ".bak")

    # Make the .new file as the new base
    os.rename(data_file + ".new", data_file)


def prompt_credentials(program_data):
    name = input("Username: ")
    if len(name) == 0:
        print("Invalid username.")
        exit()
    if name in program_data.keys():
        return prompt_password()
   
    name = create_user(program_data, name)
    return prompt_password()


def display_decaying_pass(password):
    # After the password is obtained, show it briefly and cross it out
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



# Display password accounts
# Prompt user for which one to return the password for
# TODO: I need to have a timeout if there isn't user input for a bit
def main():
    # program_data maps usernames to dictionaries mapping accounts to encrypted passwords
    # The saved program data file will be loaded into this on startup as well.
    program_data = load_data() 
    password = prompt_credentials(program_data)
    display_decaying_pass(password)
    save_data(program_data)

if __name__ == '__main__':
    main()




