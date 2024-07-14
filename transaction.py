from datetime import datetime
from math import ceil, floor

#TODO: category validation
class Transaction:
    def __init__(self, bank:str, acct_num:str, transaction_date:str, description:str, amount:str, category:str=""):
        self.bank=bank
        self.acct_num=acct_num
        self.transaction_date=transaction_date
        self.description=description
        self.amount=amount
        self.category=category
    
    @property
    def bank(self):
        return self.__bank
    
    @bank.setter
    def bank(self,bank):
        bank=bank.lower()
        if not bank in ["chase","schwab","venmo", ""]:
            raise ValueError(f"Unknown Bank: {bank}")
        self.__bank=bank
    
    @property
    def acct_num(self):
        return self.__acct_num
    
    @acct_num.setter
    def acct_num(self,acct_num):
        self.__acct_num=acct_num
    
    @property
    def transaction_date(self):
        return self.__transaction_date
    
    @transaction_date.setter
    def transaction_date(self,transaction_date):
        if "/" in transaction_date:
            self.__transaction_date=datetime.strptime(transaction_date,"%m/%d/%Y").date()
        elif "-" in transaction_date:
            self.__transaction_date=datetime.fromisoformat(transaction_date).date()
    
    @property
    def description(self):
        return self.__description
    
    @description.setter
    def description(self,description):
        self.__description=description

    @property
    def amount(self):
        return self.__amount
    
    @amount.setter
    def amount(self,amount):
        if isinstance(amount, str):
            amount=amount.replace('$','').replace(',','').replace(" ","").replace("+","")
        self.__amount=float(amount)
        if self.acct_num=="3316":
            self.__amount/=2.0

    @property
    def category(self):
        return self.__category
    
    @category.setter
    def category(self,category):
        self.__category=category.lower()
    
    def __str__(self):
        return f"{self.bank},{self.acct_num},{self.transaction_date},{self.description},{self.category},{self.amount_str()}"

    def amount_str(self):
        return f"{self.amount:.2f}"
    
    def __eq__(self, other_transaction):
        if isinstance(other_transaction, Transaction):
            return self.transaction_date == other_transaction.transaction_date and self.description == other_transaction.description and self.amount_str()==other_transaction.amount_str()
        return False
    
    def attributes_as_str_list(self):
        return [self.bank, self.acct_num, str(self.transaction_date), self.description, self.category, self.amount_str()]
    
    def ask_for_category(self):
        allowed_categories=["shopping", "groceries", "payment", "food & drink", "personal", "travel", "entertainment", "bills & utilities", "fees & adjustments", "gifts & donations", "rent", "income", "atm", "health & wellness", "gas", "home", "transfer"]
        print(f"Allowed categories: {allowed_categories}")
        new_category=input(f"{self} ... Enter Category: ").lower()
        while not new_category in allowed_categories:
            print(f"{new_category} is not an allowed category")
            print(f"Allowed categories: {allowed_categories}")
            new_category=input(f"{self} ... Enter Category: ").lower()
        
        self.category=new_category



    