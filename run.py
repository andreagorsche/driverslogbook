# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Imports to connect google sheets with python program
import gspread
from google.oauth2.service_account import Credentials

# Scope lists the APIs that the program should access in order to run.
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Create constant variables to pass creds.json file, scope and scoped creds
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

# Access the google sheet drivers log book
SHEET = GSPREAD_CLIENT.open('drivers_logbook')

# Access data in the logbook worksheet
logbook = SHEET.worksheet('logbook')

#get and print all values from the logbook worksheet
data = logbook.get_all_values() 

# import Python RegEx
import re

def validate_plate():
    """
    validating the length and the type of the number plate
    the regular Austrian plate type is: Letters, Numbers, Letters
    the custom Austrian plate type is: Letters, Letters, Numbers
    the characters for each type (regular and custom) are 8 (min) to 10 (max) including two dashes
    """
    while True:
        num_plate = input("Please enter your number plate (e.g. G-60-CYD):")
        valid_aut_1 = re.search("^(?=.{8,10}$)[A-Z]{1,2}-[0-9]{1,5}-[A-Z]{1,5}$", num_plate)
        valid_aut_2 = re.search("^(?=.{8,10}$)[A-Z]{1,2}-[A-Z]{1,5}-[0-9]{1,5}$", num_plate)

        if valid_aut_1:
            print("The number plate is of regular format. Entry correct.")
            break
        elif valid_aut_2:
            print("The number plate is a custom plate. Entry correct.")
            break
        else:
            print("invalid entry, please try again")
            continue

validate_plate()

def validate_initial_mileage():
    initial_mileage = float(input("Please enter your initial mileage (e.g. 10000):"))

    if initial_mileage > 200000:
        print(f"Your initial mileage is {initial_mileage}")
        print("This is an unusual high value. Are you sure this is correct?")
    else:
        print("Thank you for your data entry.")
      
validate_initial_mileage()