import pandas as pd # Allows us to load in the csv file.
import csv
from datetime import datetime

class CSV:
    CSV_FILE = "finance_data.csv"

    @classmethod # To have access to the class itself, meaning it can access like other class methods and class variables that we defined inside the class.
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=["date","amount","category","description"])
            df.to_csv(cls.CSV_FILE, index=False) # Not sorted by index

CSV.initialize_csv()
