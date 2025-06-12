import pandas as pd #Allows us to load in the csv file.
import csv
from datetime import datetime
from entry_data import get_amount, get_category, get_date, get_description
from entry_data import date_format
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date","amount","category","description"]

    #To have access to the class itself, meaning it can access like other class methods and class variables that we defined inside the class.
    @classmethod 
    def initialize_csv(cls):
        try:
            #Read data from CSV files into a Pandas DataFrame
            pd.read_csv(cls.CSV_FILE) 
        except FileNotFoundError:
            #Two Dimensional Data Structure
            df = pd.DataFrame(columns=cls.COLUMNS) 
            #Not sorted by index
            df.to_csv(cls.CSV_FILE, index=False) 

    #Add Entries to the File
    @classmethod
    def add_entry(cls, date, amount, category, description):
        #Store in Python Dictionary
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        #1. Opened a CSV File in append mode
        #2. 'a' (Append) - will add to the end of the file
        #3. Known as Context Manager (Class-Based) storing the open file to "csvfile"
        #4. Once the code is done inside it handles to close the file & deal with any memory leaks
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            #DictWriter - allows to write a list of dictionaries to a CSV File while perserving column headers
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            #writerow - writes a single row at a time
            writer.writerow(new_entry)
        print("Entry added succesfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        #Read data from CSV files into a Pandas DataFrame
        df = pd.read_csv(cls.CSV_FILE)
        #1. Convert all of the dates inside of the date column to a datetime object
        #2. To filter by different transactions
        df["date"] = pd.to_datetime(df["date"], format = date_format)
        #strptime() - is used to parse a string into a datetime object
        start_date = datetime.strptime(start_date, date_format)
        end_date = datetime.strptime(end_date, date_format)

        #1. Applied Mask Function - to see if we should select that row or not.
        #2. Comparing start and end dates using < and > since they are now datetime objects; this wouldn't work correctly with strings.
        #3. In Pandas, Bitwise AND (&) is used to combine multiple conditions when filtering rows in a DataFrame.
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        #Locates & keeps only the rows where the condition is True and makes a new filtered DataFrame
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range")
        else:
            #strftime() - is used to format a datetime object back to string
            print(
                f"Transactions from {start_date.strftime(date_format)} to {end_date.strftime(date_format)}"
            )
            #1. formatters is a dictionary: keys are column names, values are functions.
            #2. lambda is a small function with no name (used for short tasks)
            print(
                filtered_df.to_string(
                    index = False, formatters = {"date": lambda x: x.strftime(date_format)}
                )
            )

            #Find all rows where the Category is "Income", then add up the values in the "amount" column
            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"Total Income: ₱{total_income:.2f}")
            print(f"Total Expense: ₱{total_expense:.2f}")
            print(f"Net Savings: ₱{(total_income - total_expense):.2f}")

        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default = True,)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

#DataFrame is going to contain all of the transactions that we want to plot
def plot_transactions(df):
    #1. Index is the way in which we locate and manipulate different rows
    #2. Sort by the date and find the correct information based on the date to create the plot
    df.set_index('date', inplace = True)

    #Separate two data sets/data frame for income and expense

    #1. 'D' means daily frequency (one row per day)
    #2. Resample creates a row for each day and lets you group values by date
    #3. sum() adds up the values for each day
    #4. reindex() matches the original DataFrame's date range and fills in any missing days with 0.
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value = 0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value = 0)
    )

    #Create a new figure with a specific size
    plt.figure(figsize = (10, 5))
    #Plot income data over time in green with label "Income"
    plt.plot(income_df.index, income_df["amount"], label = "Income", color = "g")
    # Plot expense data over time in red with label "Expense"
    plt.plot(expense_df.index, expense_df["amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Expenses Over Time')
    #Show legend to label the two lines (Income and Expense)
    plt.legend()
    #Show grid lines for better readability
    plt.grid(True)
    #Display the plot
    plt.show()
    

def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date , end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

#1. This makes sure the main() function only runs when the file is run directly.
#2. It won't run automatically if the file is imported. It will only run when main() is called.
if __name__ == "__main__":
    main()