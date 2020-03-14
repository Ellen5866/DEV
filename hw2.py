
import random
class BankAccount:
    interest=0
    """
        >>> a= BankAccount('alex')
        >>> a.balance
        0
        >>> a.name
        'alex'
        >>> a.deposit(1000)
        1000
        >>> a.transfer(,200)
        800
        >>> a.withdraw(50)
        750
    """
    def __init__(self,name):
        self.name = name
        self.balance = 0

    def withdraw(self, amount):
        if self.balance - amount < 0:
            return 'Sorry, you do not have enough money.'
        else:
            return self.balance - amount

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def transfer(self, amount):
        self.balance -= amount
        return self.balance


class CheckAccount(BankAccount):
    '''
        >>> b= CheckAccount('cindy')
        >>> b.balance
        0
        >>> b.name
        'cindy'
        >>> b.deposit(1000)
        1000
        >>> b.transfer(200)
        798
        >>> b.withdraw(800)
        'Sorry, you do not have enough money.'
    '''
    transfer_fee = 2
    def __init__(self, name):
        super().__init__(name)

    def transfer(self, amount):
        return BankAccount.transfer(self,amount+self.transfer_fee)

class SavingAccount(BankAccount):
    '''
        >>> c= SavingAccount('may')
        >>> c.balance
        0
        >>> c.name
        'may'
        >>> c.deposit(1000)
        1000
        >>> c.transfer(200)
        799
        >>> c.withdraw(800)
        'Sorry, you do not have enough money.'
    '''
    interest = 0.02
    transfer_fee =1
    def __init__(self, name):
        super().__init__(name)

    def transfer(self,amount):
        return BankAccount.transfer(self,amount+self.transfer_fee)


class LimitedAccount(BankAccount):
    '''
        >>> d= LimitedAccount('jack',100)
        >>> d.balance
        0
        >>> d.name
        'jack'
        >>> d.min_balance
        100
        >>> d.deposit(1000)
        1000
        >>> d.transfer(200)
        800
        >>> d.withdraw(100)
        700
        >>> d.withdraw(650)
        'Sorry, balance below mininum.'
    '''
    def __init__(self, name, min_balance):
        super().__init__(name)
        self.min_balance = min_balance

    def withdraw(self, amount):
        self.balance = self.balance - amount
        if self.balance - amount < self.min_balance:
            return 'Sorry, balance below mininum.'
        else:
            return self.balance


from abc import *
from random import randint
import datetime
class Card(ABC):
    '''
        >>> e= Credit('marry',500)
        >>> e.changePin(1001)
        >>> e.getPin
        1001
        >>> e._Card__pin=4086
        >>> e.getPin
        4086
        >>> z= Debit('leo')
        >>> z.changePin(1020)
        >>> z.getPin
        1020
        >>> z._Card__pin=7689
        >>> z.getPin
        7689
    '''
    
    def __init__(self, name):
        self.name = name
        self.balance = 0
        self.__pin=self.__initPin
    
    @property
    def __createCard(self): 
        return random.randint(100000000000,999999999999)

    def __initPin(self):
        return random.randint(0000,9999)

    @property
    def getPin(self):
        return self.__pin

    def changePin(self, new_pin):
        self.__pin=new_pin

    @abstractmethod
    def warning(self):
        raise NotImplementedError('Subclass implements this method')
   
    @abstractmethod
    def shop(self):
        raise NotImplementedError('Subclass implements this method')
 

class Credit(Card):
    '''
        >>> f =Credit('laura',1000)
        >>> f.shop(300)
        -300
        >>> f.warning(21)
        'Your deadline is close,please pay $300 in 9 days'
        >>> f.shop(800)
        'Sorry, you have reached limit. $103 cannot be paid.'
    '''

    monthly_fee = 3
    def __init__(self,name,limit):
        self.balance = 0
        super().__init__(name)
        self.limit = limit-self.monthly_fee

    def shop(self,amount):
        self.balance = self.balance - amount
        if self.balance - amount < self.limit*(-1):
            return 'Sorry, you have reached limit. ${} cannot be paid.'.format(-1*self.balance-self.limit)
        else:
            return self.balance

    def warning(self,day):
        if day > 20:
            left = 30-day
            return 'Your deadline is close,please pay ${} in {} days'.format(-1*self.balance, left)



class Debit(Card):
    '''
        >>> g =Debit('marcus')
        >>> g.deposit(600)
        600
        >>> g.warning()
        >>> g.shop(550)
        50
        >>> g.warning()
        'Your balance is less than 100 dollars.'
        >>> g.shop(50)
        0
        >>> g.warning()
        'Sorry, you do not have enough money.'

    '''
    def __init__(self,name):
        self.balance = 0
        super().__init__(name)

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def shop(self,amount):
        self.balance=self.balance - amount
        return self.balance

    def warning(self):
        if self.balance < 100 and self.balance > 0:
            return 'Your balance is less than 100 dollars.'
        if self.balance <= 0:
            return 'Sorry, you do not have enough money.'
        else:
            return None


class Customer:
    '''
        >>> x = Customer('kay',30,'kayisok','NY')
        >>> y = Customer('eva',21,'hahuhe','TX')
        >>> y.name
        'eva'
        >>> x.getage
        30 
        >>> y.getstate
        'TX'
    '''
    def __init__(self,name, age, email, state):
        self.name = name
        self.email = email
        self.__age = age
        self.__state = state

    @property
    def getage(self):
        return self.__age

    @property   
    def getstate(self):
        return self.__state

    def changeage(self, other,new_age):
        self.getage = new_age

    def __str__(self):        
        return "customer {} from {} is {} years old, his/her email is {}".format(self.name, self.getstate,self.getage,self.email)

    __repr__=__str__
    

class Bank:
    '''
        >>> pnc = Bank()
        >>> pnc.openAccount('lay',600,BankAccount)
        >>> pnc.openAccount('harry',500,SavingAccount)
        >>> pnc.accounts[1].name
        'harry'
        >>> pnc.accounts[0].balance
        600
        >>> pnc.payInterest()
        >>> pnc.accounts[0].balance
        600
        >>> pnc.accounts[1].balance
        510.0
    '''
    def __init__(self):
        self.accounts = []
    
    def openAccount(self, name, amount, account_type=BankAccount):
        account = account_type(name)
        account.deposit(amount)
        self.accounts.append(account)
        return account
   
    def payInterest(self):
        for account in self.accounts:
            account.deposit(account.balance * account.interest)

from abc import *
class Staff(ABC):

    def __init__(self,name,position):
        self.name = name
        self.position = position

    @abstractmethod
    def readInfo(self):
        raise NotImplementedError('Subclass implements this method')

    @abstractmethod
    def changeage(self):
        raise NotImplementedError('Subclass implements this method')
   

class Manager(Staff):
    '''
        >>> a = Manager('nacy')
        >>> x = Customer('kay',30,'kayisok','NY')
        >>> a.readInfo(x)
        customer kay from NY is 30 years old, his/her email is kayisok
        >>> a.changeage(x,31)
        customer kay from NY is 30 years old, his/her email is kayisok
    '''

    def __init__(self, name):
        self.name =name

    def readInfo(self,other):
        customer = Customer (other.name,other.getage,other.email,other.getstate)
        return customer

    def changeage(self, other,new_age):
        self.getage = new_age
        customer = Customer (other.name,other.getage,other.email,other.getstate)
        return customer


        
class Teller(Staff):
    '''
        >>> d = Teller('mullen')
        >>> x = Customer('kay',30,'kayisok','NY')
        >>> d.readInfo(x)
        customer kay from NY is 30 years old, his/her email is kayisok
        >>> d.changeage(31)
        'Sorry, you do not have access to it.'
    '''
    def __init__(self, name):
        self.name = name
   
    def readInfo(self,other):
        customer = Customer (other.name,other.getage,other.email,other.getstate)
        return customer

    def changeage(self, new_age):
        return 'Sorry, you do not have access to it.'



        
    
