class BankCard:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f'Счет пополнен на: {amount}')

    def pay(self, amount):
        if 0 < amount <= self.balance:
            self.balance -=amount
            print('Операция прошла успешно')
        else:
            print('Недостаточно средств')

    def into(self):
        print(f'Владелец: {self.owner}, Баланс: {self.balance}')


card1 = BankCard("Азамат", 5000)
card2 = BankCard("Айпери", 3000)
card1.deposit(2000)
card1.pay(1500)
card2.pay(5000)
card2.pay(500)
card1.into()
card2.into()