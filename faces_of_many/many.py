# Auto create new users with defualt password

import os
import subprocess

print("Enter the username(s):\n")
usernames = [i for i in input().split()] 

def new_users(username):
    try:
        for username in usernames:
            subprocess.run(["sudo", "useradd", username], check=True)
            print(f"User {username} created successfully")
    except subprocess.CalledProcessError:
        print(f"Failed to create user {username}")