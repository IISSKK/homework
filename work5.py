# magaz = {
#     'Молоко'.lower(): 120,
#     'Хлеб'.lower(): 80,
#     'Банан'.lower(): 50,
#     'Мясо'.lower(): 500,
#     'Сок'.lower(): 80
# }

# magaz2 = input('Введите название продукта который хотите приобрести: ').lower()

# if magaz2 in magaz:
#     print(magaz[magaz2])
# else:
#     print('Товар не найден')



# students = {'Бека': 40, 'Нурс': 60, 'Артур': 80,'Егор': 90,'Али': 100 }
# bal = 0
# best_name = ''

# for name, ball in students.items():
#     if ball > bal:
#         bal = ball
#         best_name = name
# print(f'Студент с самым большим балом: {best_name}, {bal} баллов')



# a = {1, 2, 3, 4, 5, 6}
# b = {4, 5, 6, 7, 8, 9}

# print(a|b)
# print(a&b)
# print(a - b)


# numbers = [5, 2, 7, 5, 3, 2, 8, 7, 1, 5]
# new_numbers = set(numbers)
# print(len(new_numbers))
# print(new_numbers)


cities = ["Ош", "Бишкек", "Ош", "Талас", "Бишкек", "Ош", "Нарын", "Талас"]

city = {}
for i in cities:
    city[i] = city.get(i, 0) +1
print('Частота городов: ', city)

uni = set(cities)
print('Уникальные города: ',uni)
print('Количество уникальных городов: ', len(uni))