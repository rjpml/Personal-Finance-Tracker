from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

#Applied recursive function to solve smaller parts of a problem
#It must have base case (a stop sign!) to prevent endless calls
def get_date(prompt, allow_default = False):
    date_str = input(prompt)
    #Leaving the date field blank and hitting Enter will automatically set it to the current date.
    if allow_default and not date_str:
        #First Base Case
        return datetime.today().strftime(date_format)
    
    try:
        #It captures the user's input and converts it to their specified format
        valid_date = datetime.strptime(date_str, date_format)
        #Second Base Case
        #It takes the user's date input, ensures its correct conversion, and formats it as requested.
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format")
        #Return to ask the user on the date
        return get_date(prompt, allow_default)

#Applied recursive function to solve smaller parts of a problem
def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-negative or non-zero value.")
        #Base Case
        return amount
    except ValueError as e:
        print(e)
        return get_amount

def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense.): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()

def get_description():
    return input("Enter a description (optional): ")