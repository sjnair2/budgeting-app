from datetime import datetime
from file_handler import DBHandler, BankFileHandler

#TODO: search for transactions based on month and category
#TODO: monthly spending by category
#TODO: average monthly spending by category YTD
#TODO: make a config file for allowed banks, allowed categories, amount factor
#TODO: inexact category input

def main():
    transactions=[]
    db_handler=DBHandler("transaction_csvs/transactions_db.csv")
    db_handler.load_file(transactions)
    while True:
        action=int(input("(1) add transactions; (2) query by date; (0) exit: "))
        if action==0:
            break
        elif action==1:
            bank=input("Bank: ")
            acct_num=input("Last 4 digits of account: ")
            filename=input("File name: ")
            bankfile_handler=BankFileHandler(filename, bank, acct_num)
            bankfile_handler.load_file(transactions)
        elif action==2:
            start_date=datetime.fromisoformat(input("Start date (yyyy-mm-dd): ")).date()
            end_date=datetime.fromisoformat(input("End date (yyyy-mm-dd): ")).date()
            transactions_in_dates=[x for x in transactions if (x.transaction_date>=start_date and x.transaction_date<end_date)]
            unique_categories={transaction.category for transaction in transactions_in_dates}
            for category in unique_categories:
                transactions_in_category = [x for x in transactions_in_dates if x.category == category]
                print("\n"+category)
                for transaction in transactions_in_category:
                    print("\t", transaction)
    db_handler.save_file(transactions)
main()
