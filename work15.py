import sqlite3

connection = sqlite3.connect('library.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS readers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    available INTEGER DEFAULT 1,
    reader_id INTEGER,
    FOREIGN KEY(reader_id) REFERENCES readers(id)
)
''')
connection.commit()

def show_all_books():
    cursor.execute("SELECT id, title, author, year, available FROM books")
    for row in cursor.fetchall():
        status = "Доступна" if row[4] == 1 else "Выдана"
        print(f"ID: {row[0]} | Название: {row[1]} | Автор: {row[2]} | Год: {row[3]} | Статус: {status}")

def show_available_books():
    cursor.execute("SELECT id, title, author, year FROM books WHERE available = 1")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Название: {row[1]} | Автор: {row[2]} | Год: {row[3]}")

def find_book_by_title():
    title = input("Введите название книги: ")
    cursor.execute("SELECT id, title, author, year, available FROM books WHERE title LIKE ?", ('%' + title + '%',))
    for row in cursor.fetchall():
        status = "Доступна" if row[4] == 1 else "Выдана"
        print(f"ID: {row[0]} | Название: {row[1]} | Автор: {row[2]} | Год: {row[3]} | Статус: {status}")

def find_books_by_author():
    author = input("Введите автора: ")
    cursor.execute("SELECT id, title, author, year, available FROM books WHERE author LIKE ?", ('%' + author + '%',))
    for row in cursor.fetchall():
        status = "Доступна" if row[4] == 1 else "Выдана"
        print(f"ID: {row[0]} | Название: {row[1]} | Автор: {row[2]} | Год: {row[3]} | Статус: {status}")

def add_book():
    title = input("Введите название книги: ")
    author = input("Введите автора: ")
    year = int(input("Введите год выпуска: "))
    cursor.execute("INSERT INTO books (title, author, year, available) VALUES (?, ?, ?, 1)", (title, author, year))
    connection.commit()
    print("Книга успешно добавлена!")

def update_book():
    book_id = int(input("Введите ID книги для изменения: "))
    title = input("Новое название: ")
    author = input("Новый автор: ")
    year = int(input("Новый год: "))
    cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?", (title, author, year, book_id))
    connection.commit()
    print("Данные книги обновлены!")

def delete_book():
    book_id = int(input("Введите ID книги для удаления: "))
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    connection.commit()
    print("Книга удалена!")

def add_reader():
    first_name = input("Имя читателя: ")
    last_name = input("Фамилия читателя: ")
    age = int(input("Возраст читателя: "))
    cursor.execute("INSERT INTO readers (first_name, last_name, age) VALUES (?, ?, ?)", (first_name, last_name, age))
    connection.commit()
    print("Читатель зарегистрирован!")

def show_readers():
    cursor.execute("SELECT id, first_name, last_name, age FROM readers")
    for row in cursor.fetchall():
        print(f"ID: {row[0]} | Имя: {row[1]} | Фамилия: {row[2]} | Возраст: {row[3]}")

def issue_book():
    book_id = int(input("Введите ID книги для выдачи: "))
    reader_id = int(input("Введите ID читателя: "))
    cursor.execute("UPDATE books SET available = 0, reader_id = ? WHERE id = ? AND available = 1", (reader_id, book_id))
    if cursor.rowcount > 0:
        connection.commit()
        print("Книга успешно выдана читателю!")
    else:
        print("Книга не найдена или уже выдана.")

def return_book():
    book_id = int(input("Введите ID возвращаемой книги: "))
    cursor.execute("UPDATE books SET available = 1, reader_id = NULL WHERE id = ?", (book_id,))
    connection.commit()
    print("Книга возвращена в библиотеку!")

while True:
    print("\n--- БИБЛИОТЕКА ---")
    print("1. Посмотреть все книги")
    print("2. Посмотреть доступные книги")
    print("3. Найти книгу по названию")
    print("4. Найти книги по автору")
    print("5. Добавить новую книгу")
    print("6. Изменить данные книги")
    print("7. Удалить книгу")
    print("8. Зарегистрировать читателя")
    print("9. Посмотреть список читателей")
    print("10. Выдать книгу читателю")
    print("11. Вернуть книгу")
    print("0. Выход")
    
    choice = input("Выберите пункт меню: ")
    
    if choice == '1':
        show_all_books()
    elif choice == '2':
        show_available_books()
    elif choice == '3':
        find_book_by_title()
    elif choice == '4':
        find_books_by_author()
    elif choice == '5':
        add_book()
    elif choice == '6':
        update_book()
    elif choice == '7':
        delete_book()
    elif choice == '8':
        add_reader()
    elif choice == '9':
        show_readers()
    elif choice == '10':
        issue_book()
    elif choice == '11':
        return_book()
    elif choice == '0':
        connection.close()
        print("Выход из программы.")
        break
    else:
        print("Неверный выбор, попробуйте снова.")