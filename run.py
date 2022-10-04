# Imports to connect google sheets with python program
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
# import Python RegEx
import re


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
# get and print all values from the logbook worksheet
data = logbook.get_all_values() 

def take_plate_input():
    """
    validating the length and the type of the number plate
    the regular Austrian plate type is: Letters, Numbers, Letters
    the custom Austrian plate type is: Letters, Letters, Numbers
    the characters for each type are 8 (min) to 10 (max) including two dashes
    """
    num_plate = 0
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
    return num_plate

def take_initial_mileage_input():
    """
    validate if initial mileage input is reasonable
    more than 200.000 kilometers are unlikely
    """
    initial_mileage = float(input("Please enter your initial mileage in kilometers (e.g. 10000):"))
    if initial_mileage > 200000:
        print(f"Your initial mileage is {initial_mileage}")
        print("This is an unusual high value. Are you sure this is correct?")
        return take_initial_mileage_input()
    else:
        print("Thank you for your data entry.")
        return initial_mileage

def take_current_mileage_input(initial_mileage):
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
            return current_mileage

def take_travel_date_input():
    """
    check if entered date is in the format dd/mm/yyyy
    """
    date_input = input("Please enter your travel date (format: dd/mm/yyyy):")
    format_ddmmyyyy = "%d/%m/%Y"
    while True:
        try:
            travel_date = datetime.strptime(date_input, format_ddmmyyyy)
            travel_date_year = travel_date.year
            if travel_date_year > 2000:
                print("The string is a date with format " + format_ddmmyyyy)
                return travel_date
            else:
                print("The date is too old. Enter recent date")
                continue
        except ValueError:
            print("The string is not a date with format " + format_ddmmyyyy)
            print("Please try again")
            continue

def validate_journey():
    """
    validate that user entered a from and to destination
    """  
    while True:
        journey = input("Please enter your start city and destination (e.g.Vienna-Salzburg):")
        valid_journey = re.search("[A-Z]{2,20}-[A-Z]{2,20}$", journey)
        if valid_journey:
            print("The entered journey is of correct format. Entry logged.")
            return journey
        else:
            print("invalid entry, please try again")
            continue

def validate_travel_purpose():
    """
    validate that user entered either business or private as travel purpose
    """
    while True:
        travel_purpose = input("Please enter the purpose of your travel (private or business):")
        if (travel_purpose == "business" or travel_purpose == "private"):
            print(f"Your travel purpose is {travel_purpose}. Thanks for the data entry.")
            return travel_purpose
        else:
            print(f"You entered {travel_purpose}. That is not a correct data entry.")
            print("Please make sure your travel purpose is either business or private.")
            continue


def update_drivers_logbook(input_data):    
    updates spreadsheet with user input
    print("Updating sales worksheet...\n")
    logbook_worksheet = SHEET.worksheet("logbook")
    logbook_worksheet.append_row(input_data)
    print("Sales worksheet updated successfully.\n")    



def take_data_input():
    num_plate = take_plate_input()
    initial_mileage = take_initial_mileage_input()
    current_mileage = take_current_mileage_input(initial_mileage)
    travel_date = take_travel_date_input()
    journey = validate_journey()
    travel_purpose = validate_travel_purpose()
    input_data = [num_plate, initial_mileage, current_mileage, travel_date, journey, travel_purpose]
    return input_data


def main():
    """
    Run all program functions
    """
    print("Welcome to the drivers logbook.")
    input_data = take_data_input()
    update_drivers_logbook(input_data)

main()