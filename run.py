
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
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user via the terminal
    which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data, until it is valid.
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
    return sales_data   #returns validated sales data

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

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with list data provided.
    """
    print("Updating sales worksheet...\n")  #If we see this print statement before an error, we know our program got this far before it hit a problem
    sales_worksheet = SHEET.worksheet("sales") #Access the sales worksheet from the Google sheet using .worksheet method. Name corresponds to the name of the actual worksheet
    sales_worksheet.append_row(data) #Add new row to data in worksheet selected
    print("Sales worksheet updated successfully.\n") #Print this if worksheet is updated succesfully


def calculate_surplus_data(sales_row): #Passing in sales data list
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when the stock was sold out
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values() #Use gspread to get the values from the stock worksheet in the google doc
    stock_row = stock[-1] #Gets the last row of the stock spreadsheet using slice method
    
    surplus_data = [] #Add empty list for the surplus data to be put into
    for stock, sales in zip(stock_row, sales_row): #zip() method allows parsing of two or more data structures in a single loop
        surplus = int(stock) - sales #Use int() to get the integer value of the stock instead of string
        surplus_data.append(surplus) #Appends the surplus results from above to the surplus_data list
    
    return surplus_data


def main():   #Common practice to put the main function calls of a program inside a function called main
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] #sales_data is assigned the result of this list comprehension
    update_sales_worksheet(sales_data)  #Calls this funtion passing in the sales_data list
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)

    
print("Welcome to Love Sandwiches Data Automation\n")
main()
