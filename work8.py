# expenses

with open('Expenses.txt', 'w', encoding='utf-8') as f:
    f.write('Расходы:\n Продукты - 1500\n Транспорт - 300\n Интернет - 800\n  ')

with open('Expenses.txt', 'a', encoding='utf-8') as f:
    f.write('Кафе - 500\n')

with open('Expenses.txt', 'r', encoding='utf-8') as f:
    itog = f.read()
print(itog)