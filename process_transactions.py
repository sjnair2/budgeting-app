from datetime import datetime
from file_handler import DBHandler, BankFileHandler

#TODO: search for transactions based on month and category
#TODO: monthly spending by category
#TODO: average monthly spending by category YTD
#TODO: make a config file for allowed banks, allowed categories, amount factor
#TODO: inexact category input

class ProcessTransactions():
    def __init__(self, storage_service: DBHandler):
        self.__transactions=[]
        self.__storage_service=storage_service
    
    def help(self):
        print("commands")
        print("0 exit")
        print("1 add transactions")
        print("2 query by date")

    def execute(self):
        self.__storage_service.load_file(self.__transactions)
        self.help()
        while True:
            print()
            action=input("command: ")
            if action=="0":
                break
            elif action=="1":
                self.__add_transactions()
            elif action=="2":
                self.__query_by_date()
            else:
                self.help()
        self.__storage_service.save_file(self.__transactions)
    
    def __add_transactions(self):
        bank=input("Bank: ")
        acct_num=input("Last 4 digits of account: ")
        filename=input("File name: ")
        bankfile_handler=BankFileHandler(filename, bank, acct_num)
        bankfile_handler.load_file(self.__transactions)
    
    def __query_by_date(self):
        start_date=datetime.fromisoformat(input("Start date (yyyy-mm-dd): ")).date()
        end_date=datetime.fromisoformat(input("End date (yyyy-mm-dd): ")).date()
        transactions_in_dates=[x for x in self.__transactions if (x.transaction_date>=start_date and x.transaction_date<end_date)]
        unique_categories={transaction.category for transaction in transactions_in_dates}
        for category in unique_categories:
            transactions_in_category = [x for x in transactions_in_dates if x.category == category]
            print("\n"+category)
            for transaction in transactions_in_category:
                print("\t", transaction)

storage_service=DBHandler("transaction_csvs/transactions_db.csv")
application = ProcessTransactions(storage_service)
application.execute()


