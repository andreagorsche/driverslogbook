# Imports for RegEx and Pandas
import re
import pandas as pd

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
# get and print all values from the logbook worksheet
data = logbook.get_all_values()
# state subvention constant for Austria in Euro
STATE_SUB_AT = 0.42


def take_plate_input():

    """
    Validating the length and the type of the number plate
    The regular Austrian plate type is: Letters, Numbers, Letters
    The custom Austrian plate type is: Letters, Letters, Numbers
    The characters for each type are 8 (min) to 10 (max) including two dashes
    """
    num_plate = 0
    while True:
        num_plate = input("Please enter your number plate (e.g. G-60-CYD):\n")
        val_at_1 = re.search("^(?=.{8,10}$)[A-Z]{1,2}-[0-9]{1,5}-[A-Z]{1,5}$",
                             num_plate)
        val_at_2 = re.search("^(?=.{8,10}$)[A-Z]{1,2}-[A-Z]{1,5}-[0-9]{1,5}$",
                             num_plate)

        if val_at_1:
            print("The number plate is of regular format. Entry correct.")
            break
        elif val_at_2:
            print("The number plate is a custom plate. Entry correct.")
            break
        else:
            print("invalid entry, please try again")
            continue
    return num_plate


def take_initial_mileage_input():
    """
    Validate if initial mileage input is reasonable
    More than 200.000 kilometers are unlikely
    """
    try:
        print("Your initial mileage is needed.")
        initial_mileage = int(input("Please enter in km (e.g 1000):\n"))
        if initial_mileage < 0:
            print(f"Your initial mileage is {initial_mileage}")
            print("Your value is smaller than 0. Please try again?")
        elif initial_mileage > 200000:
            print(f"Your initial mileage is {initial_mileage}")
            print("Your value is unusually high. Please try again?")
            return take_initial_mileage_input()
        else:
            print("Thank you for your data entry.")
            return initial_mileage
    except ValueError:
        print("The entered data is not correct. Please try again.")


def take_current_mileage_input(initial_mileage):
    """
    Validate if current total mileage is bigger than initial mileage
    Validate if driven kilometers are manageable within a day
    (Assumption: ride of more than 1500 kilometer/day is unlikely)
    """
    while True:
        try:
            print("Your current mileage after your recent drive is needed.")
            current_mileage = int(input("Please enter in km (e.g 1000):\n"))
            mileage_difference = current_mileage - initial_mileage
            if mileage_difference < 0:
                print("The total mileage after your trip")
                print("is smaller than before.")
                print("Please check your data entry.")
                continue
            elif mileage_difference > 1500:
                print("Your entered kilometers exceed 1500km.")
                print("Are you sure this is the correct value for one trip?")
                continue
            else:
                print("Thank you for entering your driven kilometers.")
                return current_mileage
        except ValueError:
            print("The data entry was not correct. Please try again.")


def take_travel_date_input():
    """
    Convert list of string into list of int
    Within the while loop it is checked if the date input is valid
    """
    while True:
        try:
            print("Your travel date is required.")
            date_input = input("Please enter the date (format:yyyy/mm/dd):\n")
            date_list = date_input.split('/')
            date_list = [int(i) for i in date_list]
            year = date_list[0]
            month = date_list[1]
            day = date_list[2]
            if (year > 2015 and year < 2023):
                if (month > 0 and month < 13):
                    if (day > 0 and day < 32):
                        print("Date entry is correct.")
                        return date_list
                else:
                    print("Your entered date is not correct.")
                    print("Please try again.")
                    continue
        except ValueError:
            print("Data entry was not correct. Please try again.")


def validate_journey():
    """
    Validate that user entered a from and to destination
    """
    while True:
        print("Your start city and destination is required.")
        journey = input("Please enter data here (e.g.Vienna-Salzburg):\n")
        valid_journey = re.search("[A-Za-z]{2,20}-[A-Za-z]{2,20}$", journey)
        if valid_journey:
            print("The entered journey is of correct format. Entry logged.")
            return journey
        else:
            print("invalid entry, please try again")
            continue


def validate_travel_purpose():
    """
    Validate that user entered either business or private as travel purpose
    """
    while True:
        print("The purpose of your travel is required.")
        print("Only private or business is allowed as data entry.")
        travel_purpose = input("Please enter the data here:\n").lower()
        if (travel_purpose == "business" or travel_purpose == "private"):
            print(f"Your travel purpose is {travel_purpose}.")
            print("Thanks for the data entry.")
            return travel_purpose
        else:
            print(f"You entered {travel_purpose}.")
            print("That is not a correct data entry.")
            print("Please make sure your travel purpose")
            print("is either business or private.")
            continue


def take_data_input():
    """
    Calling all data input functions and returning the variable input_data
    """
    num_plate = take_plate_input()
    initial_mileage = take_initial_mileage_input()
    current_mileage = take_current_mileage_input(initial_mileage)
    date_list = (take_travel_date_input())
    journey = validate_journey()
    travel_purpose = validate_travel_purpose()
    input_data = [num_plate, initial_mileage, current_mileage,
                  *date_list, journey, travel_purpose]
    return input_data


def update_drivers_logbook(input_data):
    """
    Update spreadsheet with user input
    """
    print("Updating driver's logbook...\n")
    drivers_logbook_worksheet = SHEET.worksheet("logbook")
    drivers_logbook_worksheet.append_row(input_data)
    print("Driver's logbook updated successfully.\n")
    print(input_data)
    return input_data


def get_requested_numplate():
    """
    Get number plate user input for data retrieval
    """
    print("To calculate your driven kilometers and state subvention")
    num_plate_request = take_plate_input()
    return num_plate_request


def get_requested_year():
    """
    Get year user input for data retrieval
    """
    while True:
        try:
            print("Which year are you interested in?")
            requested_year = int(input("Please enter here (format:yyyy):\n"))
            if (requested_year > 2015 and requested_year < 2023):
                print("Date entry is correct.")
                break
            else:
                print("The entered year is not correct.")
                print("It should follow the format yyyy.")
                print("And it should between 2016 and 2022")
        except ValueError:
            print("The entered data is not correct. Please try again.")

    return requested_year


def retrieve_business_rows(num_plate_request, requested_year):
    """
    Get only rows that have the entered number plate,
    the enterd year and the purpose 'business'
    """
    df = pd.DataFrame(logbook.get_all_records())
    df.head()
    print("Retrieving data...\n")
    ret_business_rows = df.loc[(df['number plate'] == num_plate_request) &
                               (df['year'] == requested_year) &
                               (df['purpose'] == 'business')]
    print(ret_business_rows)
    return ret_business_rows


def retrieve_private_rows(num_plate_request, requested_year):
    """
    Get only rows that have the entered number plate,
    the enterd year and the purpose 'private'
    """
    df = pd.DataFrame(logbook.get_all_records())
    df.head()
    print("Retrieving data...\n")
    ret_private_rows = df.loc[(df['number plate'] == num_plate_request) &
                              (df['year'] == requested_year) &
                              (df['purpose'] == 'private')]
    print(ret_private_rows)
    return ret_private_rows


def calc_sum_private_mileage(ret_private_rows, requested_year):
    """
    Calculate the sum of the private mileage
    """
    df = ret_private_rows
    diff_private = df["current mileage"] - df["initial mileage"]
    sum_private = sum(diff_private)
    print(f"In the year {requested_year} you drove {sum_private}")
    print("kilometers for private purposes.")


def calc_sum_business_mileage(ret_business_rows, requested_year):
    """
    Calculate the sum of the business mileage
    """
    df = ret_business_rows
    diff_business = df["current mileage"] - df["initial mileage"]
    sum_business = sum(diff_business)
    print(f"In the year {requested_year} you drove {sum_business}")
    print("kilometers for business purposes.")
    return sum_business


def calc_state_sub(sum_business):
    """
    Calculate the state subvention based on the driven business kilometers.
    """
    state_sub = sum_business * STATE_SUB_AT
    print(f"For this year you have the right to claim {state_sub} Euro")
    print("in state subvention.")


def main():
    """
    Run all program functions
    """
    print("Welcome to the drivers logbook.")
    print("Do you want to enter new data or retrieve data?")
    while True:
        print("Answer with e for enter or r for retrieve.")
        initial_decision = input("Please put your answer here:")
        if initial_decision == "e":
            input_data = take_data_input()
            new_row_logbook = update_drivers_logbook(input_data)
            break
        elif initial_decision == "r":
            num_plate_request = get_requested_numplate()
            requested_year = get_requested_year()
            ret_business_rows = retrieve_business_rows(num_plate_request,
                                                       requested_year)
            ret_private_rows = retrieve_private_rows(num_plate_request,
                                                     requested_year)
            sum_business = calc_sum_business_mileage(ret_business_rows,
                                                     requested_year)
            calc_sum_private_mileage(ret_private_rows, requested_year)
            calc_state_sub(sum_business)
            break
        else:
            print("Sorry. That was not a correct data entry.")
            print("Please try again.")
            continue


main()
