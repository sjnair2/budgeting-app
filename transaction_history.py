import csv
from transaction import Transaction
from operator import attrgetter


class TransactionHistory:
    def __init__(self, db_filename: str):
        self.__transactions=[]
        self.read_db(db_filename)

    def read_db(self, db_filename: str):
        with open(db_filename) as new_file:
            for line in csv.reader(new_file, delimiter=","):
                bank, acct_num, transaction_date, description, category, amount = line[0], line[1], line[2], line[3], line[4], line[5]
                my_transaction=Transaction(bank, acct_num, transaction_date, description, amount, category)
                self.__transactions.append(my_transaction)
    
    def add_transactions(self, bank_filename:str, bank:str, acct_num:str):
        line_num=0
        num_new_transactions=0
        with open(bank_filename) as new_file:
            for line in csv.reader(new_file, delimiter=","):
                line_num+=1
                if bank=="chase" and line_num>1:
                    transaction_date, description, category, amount=line[0], line[2], line[3], line[5]
                elif bank=="schwab" and line_num>1:
                    transaction_date, description, withdrawal, deposit, category=line[0], line[4], line[5], line[6], ""
                    if withdrawal!="":
                        amount="-"+withdrawal
                    else:
                        amount=deposit
                elif bank=="venmo" and line_num>4:
                    if line[1]=="":
                        break
                    transaction_date, description, amount, category=line[2], line[5], line[8], ""
                else:
                    continue

                new_transaction=Transaction(bank, acct_num, transaction_date, description, amount, category)

                if not new_transaction in self.__transactions:
                    if new_transaction.category=="":
                        new_transaction.ask_for_category()
                    self.__transactions.append(new_transaction)
                    num_new_transactions+=1
        self.__transactions.sort(key=attrgetter('transaction_date', 'bank', 'acct_num'))
        print(num_new_transactions, "transactions added.")