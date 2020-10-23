# USER INTERFACE 
import random
import sqlite3
#import database // FOR PERSONAL SOLUTION

# Globals
ACCOUNTS = [] # Temp storage

MENU_PROMPT = """
1. Create an account
2. Log into account
0. Exit"""

LOGGED_IN_PROMPT = """
1. Balance
2. Log out
0. Exit"""

CREATE_TABLE = """CREATE TABLE IF NOT EXISTS card (
    id INTEGER PRIMARY KEY,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);"""

# DATABASE FUNCTIONS
def connect():
    # Create connection to DB
    return sqlite3.connect("card.s3db")

def create_table(connection):
    # create Cursor object
    cursor = connection.cursor()
    cursor.execute(CREATE_TABLE)

# USER INTERFACE FUNCTIONS
def menu():
    connection = connect()
    create_table(connection)
    while (user_command := input(MENU_PROMPT)) != '0':
        if user_command == '1':
            create_account(connection)
        elif user_command == '2':
            login()
        else:
            print("Unknown command. Please try again.")

    print("Bye!")


# Generates a pincode with sequence of 4 digits from 0000 to 9999
# return str representation of PIN CODE
def generate_pincode():
    pin_code = random.randint(0, 9999)
    # pad the PIN with leading 0s
    pin_code = str(pin_code).zfill(4)

    return pin_code


def create_card():
    bank_inn = 400000
    # generate a 9 digit account number
    account_num = generate_account_num()
    while True:
        if is_account_unique(account_num):
            break
        else:
            account_num = generate_account_num()

    # generate a check sum digit
    check_sum = random.randint(0, 9)

    card_number = str(bank_inn) + str(account_num) + str(check_sum)
    # pass card number into Luhn Algorithm
    card = luhn_algorithm(card_number)
    return card


def luhn_algorithm(cc_number):
    # split into a list / array of string digits
    my_split = list(cc_number)
  
    my_split.pop()

    # multiply every odd digit by 2
    for i in range(0,len(my_split), 2):
        my_split[i] = int(my_split[i]) * 2
    
    #iterate over list subtract nums > 9
    for i in range(len(my_split)):
        if int(my_split[i]) > 9:
            my_split[i] = str(int(my_split[i]) - 9)
  
    # add all numbers to find control number
    total = 0
    for i in range(len(my_split)):
        total = total + int(my_split[i])

    result = list(cc_number)
    # check if total is divisible by 10
    if total % 10 == 0:
        result[len(cc_number)-1] = '0'
        return ''.join(result)

    checksum = 0
    # repeat n times until the checknumber
    while True:
        checksum += 1
        total += 1
        if total % 10 == 0:
            break
    
    # replace the last index with checksum
    result[len(cc_number)-1] = str(checksum)
    #print(f"Result: {result}")
    return ''.join(result)


def generate_account_num():
    account_number = ""
    for i in range(9):
        random_num = random.randint(0, 9)
        account_number += str(random_num)
    print(account_number)
    return account_number


def is_account_unique(account_num):
    if account_num in ACCOUNTS:
        return False
    else:
        return True


# Generates card number and then generates a pin_code belonging to the generated card number
def create_account(connection):
    user_card = create_card()
    user_pin = generate_pincode()

    new_account = {"account number": user_card, "pin": user_pin, "balance": 0}
    ACCOUNTS.append(new_account)

    # INSERT CARD INTO card TABLE
    #cursor.execute("INSERT INTO card (number, pin) VALUES(?, ?)", (user_card, user_pin))
    #connection.commit()

    print(f"Your card has been created\nYour card number:\n{user_card}")
    print(f"Your card PIN:\n{user_pin}\n")

    return None


def login():
    print("Please enter your login credentials.")
    card_number = input("Enter your card number:")
    card_pin = input("Enter your PIN:")

    # Check if the account exists in list of accounts
    for account in ACCOUNTS:
        if account["account number"] == card_number and account["pin"] == card_pin:
            print("You have successfully logged in!")
            user_menu(account)

    print("Wrong card number or PIN!\n")


def get_account_balance(user_account):
    print(f"Balance: {user_account['balance']}")
    user_menu(user_account)


def user_menu(user_account):
    print(LOGGED_IN_PROMPT)
    user_command = input()
    while user_command != '0':
        if user_command == '1':
            get_account_balance(user_account)
        elif user_command == '2':
            # go back to main menu
            print("You have successfully logged out!")
            menu()

        else:
            print("Please enter a valid command!\n")
            
        user_command = input()

    print("Bye!")
    exit(1)


# Testing Methods
def show_accounts():
    for account in ACCOUNTS:
        print(account)


if __name__ == '__main__':
    menu()

