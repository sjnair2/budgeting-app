import csv
from transaction import Transaction

#TODO: input validation and inexact category input
#TODO: search for transactions based on month and category
#TODO: monthly spending by category
#TODO: average monthly spending by category YTD
#TODO: make amount factor configurable
#TODO: prompt for category if it is empty
#TODO: validate bank at prompt?

def read_bankfile(transactions:list, filename:str, bank:str, acct_num:str):
    line_num=1
    with open(filename) as new_file:
        for line in csv.reader(new_file, delimiter=","):
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

            if not new_transaction in transactions:
                print("alert")

            line_num+=1

def read_transactions_db(transactions:list):
    with open("transactions_db.csv") as new_file:
        for line in csv.reader(new_file, delimiter=","):
            bank, acct_num, transaction_date, description, category, amount = line[0], line[1], line[2], line[3], line[4], line[5]
            my_transaction=Transaction(bank, acct_num, transaction_date, description, amount, category)
            transactions.append(my_transaction)

def write_transactions_db(transactions:list):
    with open("transactions_db.csv", "w") as my_file:
        transaction_writer = csv.writer(my_file, delimiter=',')
        for transaction in transactions:
            line=transaction.attributes_as_str_list()
            transaction_writer.writerow(line)

def main():
    transactions=[]
    read_transactions_db(transactions)
    while True:
        action=int(input("(1) add transactions; (2) exit: "))
        if action==2:
            break
        elif action==1:
            bank=input("Bank: ")
            acct_num=input("Last 4 digits of account: ")
            filename=input("File name: ")
            read_bankfile(transactions, filename, bank, acct_num)
            print("Added transactions.")
    write_transactions_db(transactions)
main()
