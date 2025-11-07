class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be > 0")
        self.__balance += amount

    def get_balance(self):
        return self.__balance


acc = Account("Eric", 300000)

try:
    print(acc.balance)
except AttributeError as e:
    print(e)

print(acc.get_balance())
