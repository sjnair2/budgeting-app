import csv
from transaction import Transaction

#TODO: search for transactions based on month and category
#TODO: monthly spending by category
#TODO: average monthly spending by category YTD
#TODO: make a config file for allowed banks, allowed categories, amount factor
#TODO: inexact category input

def read_bankfile(transactions:list, filename:str, bank:str, acct_num:str):
    line_num=0
    num_new_transactions=0
    with open(filename) as new_file:
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

            if not new_transaction in transactions:
                if new_transaction.category=="":
                    new_transaction.ask_for_category()
                transactions.append(new_transaction)
                num_new_transactions+=1
    print(num_new_transactions, "transactions added.")

def read_transactions_db(transactions:list):
    with open("transaction_csvs/transactions_db.csv") as new_file:
        for line in csv.reader(new_file, delimiter=","):
            bank, acct_num, transaction_date, description, category, amount = line[0], line[1], line[2], line[3], line[4], line[5]
            my_transaction=Transaction(bank, acct_num, transaction_date, description, amount, category)
            transactions.append(my_transaction)

def write_transactions_db(transactions:list):
    with open("transaction_csvs/transactions_db.csv", "w") as my_file:
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
    write_transactions_db(transactions)
main()
