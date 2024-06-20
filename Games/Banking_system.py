from abc import ABC, abstractmethod

import random
import datetime
import math

#Transaction class to keep the records
class Transaction(ABC):
  def __init__(self, customerId, tellerId):
    self._customerId = customerId
    self._tellerId = tellerId

  def get_customer_id(self):
    return self._customerId

  def get_teller_id(self):
    return self._tellerId

  @abstractmethod
  def get_transaction_description(self):
    pass

#Deposit class 
class Deposit(Transaction):
  def __init__(self, customerId, tellerId, amount):
    super().__init__(customerId, tellerId)
    self._amount = amount

  #get the deposit description
  def get_transaction_description(self):
    return f'Teller {self.get_teller_id()} deposited {self._amount} to account {self.get_customer_id()}'

# withdrawal class
class Withdrawal(Transaction):
  def __init__(self, customerId, tellerId, amount):
    super().__init__(customerId, tellerId)
    self._amount = amount

  def get_transaction_description(self):
    return f'Teller {self.get_teller_id()} withdrew {self._amount} from account {self.get_customer_id()}'

# when new account is opened
class OpenAccount(Transaction):
  def __init__(self, customerId, tellerId):
    super().__init__(customerId, tellerId)

  def get_transaction_description(self):
    return f'Teller {self.get_teller_id()} opened account {self.get_customer_id}'

# Teller class 
class BankTeller:
  def __init__(self, id):
    self._id = id
  
  def get_id(self):
    return self._id

# given our bank will have many branches so let's create the bankbranch class 
# so all the branch are in sync and function as the real time banking system

class BankBranch:
  def __init__(self, address, cash_on_hand, bank_system):
    self._address = address
    self._cash_on_hand = cash_on_hand
    self._bank_system = bank_system
    self._tellers = []


  def add_teller(self, teller):
    self._tellers.append(teller)

  def _get_available_teller(self):
    index = round(random.random() * (len(self._tellers)-1))
    return self._tellers[index].get_id()

  def open_account(self, customer_name):
    if not self._tellers:
      raise ValueError('Branch does not have any tellers')
    teller_id = self._get_available_teller()
    return self._bank_system.open_account(customer_name, teller_id)

  def deposit(self, customer_id, amount):
    if not self._tellers:
      raise ValueError('Branch does not have any tellers')
    teller_id = self._get_available_teller()
    self._bank_system.deposit(customer_id, teller_id, amount)


  def withdraw(self, customer_id, amount):
    if amount > self._cash_on_hand: # if we don't have cash
      raise ValueError('Branch does not have enough cash')
    if not self._tellers: # if we don't have any teller available
      raise ValueError('Branch does not have any tellers')
    self._cash_on_hand  -= amount
    teller_id = self._get_available_teller()
    self._bank_system.withdraw(customer_id, teller_id, amount)

  def collect_cash(self, ratio): # each day we deposit some cash to the HeadQuaters
    cash_to_collect = round(self._cash_on_hand * ratio)
    self._cash_on_hand -= cash_to_collect
    return cash_to_collect

  def provide_cash(self, amount):
    self._cash_on_hand += amount

class BankAccount:
  def __init__(self, customerId, name, balance):
    self._customerId = customerId
    self._name = name
    self._balance = balance

  def get_balance(self):
    return self._balance

  def deposit(self, amount):
    self._balance += amount

  def withdraw(self, amonut):
    self._balance -= amount


#Bank system

class BankSystem:
  def __init__(self, accounts, transactions):
    self._accounts = accounts
    self._transactions = transactions

  def get_account(self, customerId):
    return self._accounts[customerId]

  def get_accounts(self):
    return self._accounts

  def get_transactions(self):
    return self._transactions

  def open_account(self, customer_name, teller_id):
    # create account
    customerId = len(self.get_accounts())
    account = BankAccount(customerId, customer_name, 0)
    self._accounts.append(account)


    # log transactions
    transaction = OpenAccount(customerId, teller_id)
    self._transactions.append(transaction)
    return customerId

  def deposit(self, customer_id, teller_id, amount):
    account = self.get_account(customer_id)
    account.deposit(amount)

    transaction = Deposit(customer_id, teller_id, amount)
    self._transactions.append(transaction)

  def withdraw(self, customer_id, teller_id, amount):
    if amount > self.get_account(customer_id).get_balance():
      raise Exception('Insufficienct funds')
    account = self.get_account(customer_id)
    account.withdraw(amount)

    transaction = Withdrawal(customer_id, teller_id, amount)
    self._transactions.append(transaction)


# Bank class

class Bank:
  def __init__(self, branches, bank_system, total_cash):
    self._branches = branches
    self._bank_system = bank_system
    self._total_cash = total_cash

  def add_branch(self, address, initial_funds):
    branch = BankBranch(address, initial_funds, self._bank_system)
    self._branches.append(branch)
    return branch

  def collect_cash(self, ratio):
    for branch in self._branches:
      cash_collected = branch.collect_cash(ratio)
      self._total_cash += cash_collected

  def print_transactions(self):
    for transaction in self._bank_system.get_transactions():
      print(transaction.get_transaction_description())

bankSystem = BankSystem([], [])
bank = Bank([], bankSystem, 100000)

branch1 = bank.add_branch('563 Harely Drive', 1000)
branch2 = bank.add_branch('234 Riverside Drive', 1000)

branch1.add_teller(BankTeller(1))
branch1.add_teller(BankTeller(2))
branch1.add_teller(BankTeller(3))

branch2.add_teller(BankTeller(4))
branch2.add_teller(BankTeller(5))
branch2.add_teller(BankTeller(6))

customerId1 = branch1.open_account('Jone Dayton')
customerId2 = branch2.open_account('Jason Duo')
customerId3 = branch2.open_account('Rayn Brim')

branch1.deposit(customerId1, 100)
branch2.deposit(customerId2, 100)
branch2.deposit(customerId3, 100)

bank.collect_cash(0.1)
bank.print_transactions()

               

