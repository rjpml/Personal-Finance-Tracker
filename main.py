import pandas as pd #Allows us to load in the csv file.
import csv
from datetime import datetime
from entry_data import get_amount, get_category, get_date, get_description
from entry_data import date_format

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
        # Opened a CSV File in append mode
        # "a" (Append) - will add to the end of the file
        # Known as Context Manager (Class-Based) storing the open file to "csvfile"
        # Once the code is done inside it handles to close the file & deal with any memory leaks
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
        df["date"] = pd.to_datetime()
        #Convert all of the dates inside of the date column to a datetime object
        #To filter by different transactions
        df["date"] = pd.to_datetime(df["date"], format = date_format)

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default = True,)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

add()