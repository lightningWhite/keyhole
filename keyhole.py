# Password Manager
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

uname_file = ".unames.txt"


def prompt_password():
    password = getpass.getpass()
    return password

def create_user(username=""):
    do_create = input("Username doesn't exist. Create one? [Y/n] ")
    if do_create == 'Y' or do_create == 'y':
        ans = input(f"Is the name '{username}' okay? [Y/n] ")
        if ans == 'n' or ans == 'N':
            valid = 0
            while valid == 0:
                username = input("Enter a new username: ")
                # Check if user exists
                if os.path.exists(uname_file):
                    with open(uname_file) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                        if s.find(name.encode()) != -1:
                            print("That username already exists.")
                        else:
                            valid = 1

    else:
        print("Exiting...")
        exit()

    # Append the new username to the username file
    f = open(uname_file, "a")
    f.write(username + '\n')

    return username
       

def prompt_credentials():
    name = input("Username: ")
    if len(name) == 0:
        print("Invalid username.")
        exit()
   
    # Check if user exists
    if os.path.exists(uname_file):
        with open(uname_file) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(name.encode()) != -1:
                # get password from the user
                return prompt_password()
            
    name = create_user(name)
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
       time.sleep(1/(i+1))
    
       # Clear the line in the terminal
       sys.stdout.write("\033[K")



# Display password accounts
# Prompt user for which one to return the password for
# TODO: I need to have a timeout if there isn't user input for a bit
def main():
    password = prompt_credentials()
    display_decaying_pass(password)

if __name__ == '__main__':
    main()




