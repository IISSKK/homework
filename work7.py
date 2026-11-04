# with open('students.txt', 'w', encoding='utf-8') as f:
#     f.write('Антон\nНаташа\nСергей\nНастя\nАртур')

# with open('students.txt', 'r', encoding='utf-8') as f:
#     name = f.read()
#     print(name)

# diary = input('Пишите в заметки: ')

# with open('diary.txt', 'a', encoding='utf-8') as f:
#     diary_input = f.write(diary + '\n')

# with open('diary.txt', 'r', encoding='utf-8') as f:
#     diary_itog = f.read()
#     print(diary_itog)

with open('text.txt', 'w', encoding='utf-8') as f:
    f.write('Если вы хотите изучить Python то он давольно легкий в изучений и используется в широко известных компаниях')

file_name = 'text.txt'

text_input = input('Введите слово для поиска: ')

with open('text.txt', 'r', encoding='utf-8') as f:
    text_itog = f.read()
    if text_input in text_itog:
        print(f'Слово который вы искали: {text_input}! Находиться в файле: {file_name}')
    else:
        print('Слово не найдено')