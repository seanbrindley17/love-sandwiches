import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():   #Runs a while loop that asks the user for data
    """
    Get sales figures input from the user
    """
    while True:     #Loop which will only end when correct data is given
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",") #Converts string of data into list of values
        
        if validate_data(sales_data):   #Calls validate data function, passing the sales data list
            print("Data is valid")  #Checks for errors, if none are found then this is printed
            break                   #and the while loop is stopped

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int, 
    or if there aren't exactly 6 values.
    """
    
    try:
        [int(value) for value in values] #Trying to convert each value in the values list into an integer
        if len(values) != 6:    #Check if the values list doesn't have 6 values
            raise ValueError(   #Raise ValueError
                f"Exactly 6 values required, you provided {len(values)}" #Prints this error to terminal with the length of the value list inputted
            )
    except ValueError as e: #e is generic error placement letter
        print(f"Invalid data {e}, please try again.\n") #Prints this error if invalid data type is added
        return False    #If either error is triggered, false is returned
    
    return True     #If data input is correct, true is returned

get_sales_data()
