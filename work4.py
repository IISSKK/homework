# ste = int(input('Введите на каком этаже вы находитесь: '))
# ste2 = int(input('Введите на какой этаж хотите попасть: '))

# if ste2 > ste:
#     print('Вы поехали вверх')
# elif ste > ste2:
#     print('Вы поехали вниз')
# else:
#     print('Вы в нужном этаже')

# 
# 
# for i in range(1, 51):
#     if i % 4 == 0:
#         continue
#     print(i)



# warm_day = 0

# for i in range(7):
#     g = int(input('Введите температуру за последние 7 дней: '))
#     if g < 0:
#         print('Мороз')
#     elif 0 <= g <= 20:
#         print('Прохладно')
#     else:
#         warm_day += 1
#         print('Тепло')

# print(f'Количество теплых дней: {warm_day}')



# biggest = int(input('Введите первое число: '))

# for i in range(6):
#     new_num = int(input('Введите следующее число: '))
#     if new_num > biggest:
#         biggest = new_num
# print(biggest)



# age_18 = 0
# age = 0

# for i in range(10):
#     age2 = int(input('Напишите возраст: '))
#     if age2 < 18:
#         age += 1
#     elif age2 >= 18:
#         age_18 += 1
# print(f'Число совершеннолетних поситителей: {age_18}! Число несовершеннолетних поситителей: {age}!')