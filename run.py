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

initial_mileage = float(input("Please enter your initial mileage in kilometers (e.g. 10000):"))

def validate_initial_mileage():
    """
    validate if initial mileage input is reasonable
    more than 200.000 kilometers are unlikely
    """
    if initial_mileage > 200000:
        print(f"Your initial mileage is {initial_mileage}")
        print("This is an unusual high value. Are you sure this is correct?")
    else:
        print("Thank you for your data entry.")
    
validate_initial_mileage()


def validate_current_mileage():
    """   
    validate if current total mileage is bigger than initial mileage
    validate if driven kilometers are manageable within a day
    (assumption that one will most likely not drive more than 1500 kilometer a day)
    """  
    while True:
        current_mileage = float(input("Please enter your total mileage after your recent ride:"))
        mileage_difference = current_mileage - initial_mileage
        if  ((mileage_difference) < 0):
            print("Your total mileage after your trip is smaller than before.")
            print("Please check your data entry.")
            continue
        elif ((mileage_difference) > 1500):
            print("Your entered kilometers exceed 1500km.")
            print("Are you sure this is the correct value for one trip?")
            continue
        else:
            print("Thank you. Your driven kilometers were added to the system.")
            break

validate_current_mileage()

#import datetime to validate date entry

from datetime import datetime

def check_valid_date():
    """
    check if entered date is in the format dd/mm/yyyy
    """
    date_input = input("Please enter your travel date (format: dd/mm/yyyy):")
    format_ddmmyyyy = "%d/%m/%Y"
    while True:
        try:
            travel_date = datetime.strptime(date_input, format_ddmmyyyy)
            print("The string is a date with format " + format_ddmmyyyy)
            break
        except ValueError:
            print("The string is not a date with format " + format_ddmmyyyy)
            print("Please try again")
            continue

check_valid_date()
