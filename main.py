import pandas as pd #Allows us to load in the csv file.
import csv
from datetime import datetime
from entry_data import get_amount, get_category, get_date, get_description

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

def add():
    CSV.initialize_csv


CSV.initialize_csv()
CSV.add_entry("06-10-2025", 125.65, "Income", "Salary")