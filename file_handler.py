import csv
from transaction import Transaction

class DBHandler:
    def __init__(self, filename):
        self.__filename=filename

    def load_file(self, transactions: list):
        with open(self.__filename) as new_file:
            for line in csv.reader(new_file, delimiter=","):
                bank, acct_num, transaction_date, description, category, amount = line[0], line[1], line[2], line[3], line[4], line[5]
                my_transaction=Transaction(bank, acct_num, transaction_date, description, amount, category)
                transactions.append(my_transaction)
    
    def save_file(self, transactions: list):
        with open(self.__filename, "w") as my_file:
            transaction_writer = csv.writer(my_file, delimiter=',')
            for transaction in transactions:
                line=transaction.attributes_as_str_list()
                transaction_writer.writerow(line)

class BankFileHandler:
    def __init__(self, filename: str, bank: str, acct_num: str):
        self.__filename=filename
        self.__bank=bank
        self.__acct_num=acct_num

    def load_file(self, transactions: list):
        line_num=0
        num_new_transactions=0
        with open(self.__filename) as new_file:
            for line in csv.reader(new_file, delimiter=","):
                line_num+=1
                if self.__bank=="chase":
                    new_transaction=self.__read_chase_line(line, line_num)
                elif self.__bank=="schwab":
                    new_transaction=self.__read_schwab_line(line, line_num)
                elif self.__bank=="venmo":
                    new_transaction=self.__read_venmo_line(line, line_num)

                if new_transaction == None:
                    continue

                if not new_transaction in transactions:
                    if new_transaction.category=="":
                        new_transaction.ask_for_category()
                    transactions.append(new_transaction)
                    num_new_transactions+=1
        print(num_new_transactions, "transactions added.")

    def __read_chase_line(self, line: list, line_num: int):
        if line_num>1:
            transaction_date, description, category, amount = line[0], line[2], line[3], line[5]
            return Transaction(self.__bank, self.__acct_num, transaction_date, description, amount, category) 
        return None
    
    def __read_schwab_line(self, line: list, line_num:int):
        if line_num>1:
            transaction_date, description, withdrawal, deposit, category=line[0], line[4], line[5], line[6], ""
            if withdrawal!="":
                amount="-"+withdrawal
            else:
                amount=deposit
            return Transaction(self.__bank, self.__acct_num, transaction_date, description, amount, category)
        return None
    
    def __read_venmo_line(self, line: list, line_num: int):
        if line_num>4:
            if line[1]=="":
                return None
            transaction_date, description, amount, category=line[2], line[5], line[8], ""
            return Transaction(self.__bank, self.__acct_num, transaction_date, description, amount, category)
        return None