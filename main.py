import matplotlib.pyplot as plt
import pandas as pd
import csv
from data_validation import *
from datetime import datetime


class CSV:
    CSV_file = "finance_management.csv"

    @classmethod
    def initalizeCSV(cls):
        try:
            pd.read_csv(cls.CSV_file)
        except FileNotFoundError:
            db = pd.DataFrame(columns=['date', 'Amount', 'Type', 'Description'])
            db.to_csv(cls.CSV_file, index = False)

    @classmethod
    def addTransaction(cls, date, amount, type, description):
        newEntry = {
            "date": date,
            "Amount" : amount,
            "Type": type,
            "Description": description
        }
        with open(cls.CSV_file, "a", newline = "") as csvfile:
            writter = csv.DictWriter(csvfile, fieldnames = ['date', 'Amount', 'Type', 'Description'])
            writter.writerow(newEntry)
        print("Entry added successfully... ")

    @classmethod
    def showDetailsinRange(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_file)
        df['date'] = pd.to_datetime(df["date"], format = '%d-%m-%Y')
        start_date = datetime.strptime(start_date, '%d-%m-%Y')
        end_date = datetime.strptime(end_date, '%d-%m-%Y')

        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        new_df = df.loc[mask]

        if(new_df.empty):
            print("\nno transactino in this date range")
        else:
            print("\nYour transaction are :")
            print(new_df.to_string(index = False, formatters = {'date' : lambda x: x.strftime('%d-%m-%Y')}))

            tot_income = new_df[new_df['Type'] == 'Credit']["Amount"].sum()
            tot_expense = new_df[new_df['Type'] == 'Debit']["Amount"].sum()
            print(f'\nYour details since {start_date.strftime('%d-%m-%Y')} to {end_date.strftime('%d-%m-%Y')} are \nTotal Expense: {tot_expense} \nTotal income is {tot_income}')
            print(f'Net {"saving" if (tot_income - tot_expense) > 0 else "debt"} is: {abs(tot_income - tot_expense)}')

            return new_df
        
    @classmethod
    def showAllDetails(cls):
        new_df = pd.read_csv(cls.CSV_file)
        new_df['date'] = pd.to_datetime(new_df['date'], errors='coerce', format='%d-%m-%Y')

        if new_df.empty:
            print("\nNo transactions are here")
        else:
            print("\nYour transactions are:")
            
            print(new_df.to_string(index=False, formatters={'date': lambda x: x.strftime('%d-%m-%Y') if not pd.isnull(x) else ''}))

            tot_income = new_df[new_df['Type'] == 'Credit']["Amount"].sum()
            tot_expense = new_df[new_df['Type'] == 'Debit']["Amount"].sum()
            
            print(f'\nYour details are \nTotal Expense: {tot_expense} \nTotal Income: {tot_income}')
            print(f'Net {"saving" if (tot_income - tot_expense) > 0 else "debt"} is: {abs(tot_income - tot_expense)}')

            return new_df
    

def showPlot(df):
    df.set_index('date', inplace = True)

    credit_df = (df[df['Type'] == "Credit"].resample('D').sum().reindex(df.index, fill_value = 0))
    debit_df = (df[df['Type'] == "Debit"].resample('D').sum().reindex(df.index, fill_value = 0))

    plt.figure(figsize = (10,5))
    plt.plot(credit_df.index, credit_df.Amount, label = 'Credits', color = "b")
    plt.plot(debit_df.index, debit_df.Amount, label = 'Debits', color = 'g')
    plt.xlabel("Dates")
    plt.ylabel("Amount")
    plt.legend()
    plt.title("Credits and Debits Details")
    plt.grid(True)
    plt.show()


def add():
    CSV.initalizeCSV()
    date = get_date("Enter Date in dd-mm-yyyy format or click 'enter' to pass today's date: ", default = False)
    amount = get_amount()
    category = get_category()
    desc = get_desciption()

    CSV.addTransaction(date, amount, category, desc)



def showAllDetails():

    CSV.initalizeCSV()
    new_df = CSV.showAllDetails()
    if input("\nWould you like to see grpah for details above (y/n) ?").upper() == 'Y' :
        showPlot(new_df)    



def show_details():
    CSV.initalizeCSV()
    start_date = get_date("Enter a valid start date in dd-mm-yyyy format: ")
    end_date = get_date("Enter a valid end date in dd-mm-yyyy format: ")
    new_df = CSV.showDetailsinRange(start_date, end_date)

    if input("\nWould you like to see grpah for details above (y/n) ?").upper() == 'Y' :
        showPlot(new_df)


    pass

# add()
#CSV.showDetailsinRange("01-01-2000", "30-10-2024")

# CSV.initalizeCSV()
# CSV.addTransaction("03-10-2005", 3456.00, "Expense", "Picnic")

def main():
    while True:
        print('''\nWelcome to Finance Tracker...
            ->  Press 1 to add expense 
            ->  Press 2 to view your expenses within a date range
            ->  Press 3 to view all transaction details  
            ->  Press 0 to exit
              Thank you :)''')
        
        res = input()

        if(res == '1'):
            add()
        elif(res == '2'):
            show_details()
        elif(res == '3'):
            showAllDetails()
        elif(res == '0'):
            print ("\n Exiting ...")
            break
        else:
            print("Please Enter a valid number")

if(__name__ == "__main__"):
    main()