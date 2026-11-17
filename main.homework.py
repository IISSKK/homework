from abc import ABC, abstractmethod
import sqlite3
from datetime import date

# имя файла базы вынес в константу, чтобы поменять его в одном месте
DB_NAME = "library.db"


# декоратор: оборачивает метод и перед запуском печатает его название.
# сделал так, чтобы не писать print в каждом методе бд, достаточно
# поставить @log_execution. *args и **kwargs нужны чтобы он подходил
# к любой функции, а return нужен чтобы не потерять результат
# (например id из add_book)
def log_execution(func):

    def wrapper(*args, **kwargs):
        print(f"[LOG] Выполнение метода: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# миксин - маленький класс с одной способностью (сделать словарь из объекта),
# его подмешивают к другим классам через множественное наследование.
# приватные атрибуты хранятся как _Book__year, поэтому ключ обрезаю
# по "__", чтобы в словаре было просто year
class JsonExportMixin:

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            clean_key = key.split("__")[-1].lstrip("_")
            result[clean_key] = value
        return result


# абстрактный класс (ABC): объект LibraryItem создать нельзя, он только
# задаёт правило, что у любого предмета библиотеки должен быть get_info().
# название приватное (__title) и меняется только через property, где
# стоит проверка. в __init__ присваиваю через self.title, а не напрямую,
# чтобы пустое название не прошло даже при создании
class LibraryItem(ABC):
    def __init__(self, title):
        self.__title = None
        self.title = title

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Название должно быть непустой строкой")
        self.__title = value.strip()

    @abstractmethod
    def get_info(self):
        pass


# Book наследуется от двух классов: от LibraryItem берёт название и
# абстрактный метод, от миксина берёт to_dict. super().__init__(title)
# передаёт название родителю, чтобы не дублировать его проверку.
# год сделан так же как название (приватный + property), через self.year
# чтобы сработала валидация
class Book(JsonExportMixin, LibraryItem):
    def __init__(self, title: str, author: str, year: int):
        super().__init__(title)
        self.author = author
        self.year = year

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        if not self.validate_year(value):
            raise ValueError(f"Неверный год выпуска: {value}")
        self.__year = value

    # staticmethod, потому что ему не нужны ни self ни cls, он просто
    # проверяет число. лежит в классе потому что относится к книгам.
    # сравниваю с текущим годом чтобы нельзя было ввести год из будущего
    @staticmethod
    def validate_year(year):
        return isinstance(year, int) and 0 < year <= date.today().year

    # classmethod - второй способ создать объект, из словаря (нужен при
    # чтении из бд). cls это сам класс, поэтому в AudioBook этот же метод
    # создаст уже аудиокнигу
    @classmethod
    def from_data(cls, data: dict):
        return cls(data["title"], data["author"], data["year"])

    def get_info(self):
        return f"Книга: «{self.title}», автор: {self.author}, год: {self.year}"

    # __str__ вызывается в print(book), отдаёт get_info, поэтому у
    # аудиокниги автоматически будет свой вывод
    def __str__(self):
        return self.get_info()

    # две книги считаю одинаковыми если совпадает название (без учёта
    # регистра). NotImplemented - чтобы с другими типами не сравнивалось.
    # __hash__ пришлось добавить, потому что без него после __eq__
    # книги нельзя класть в set и dict. хеш по тому же полю что и равенство
    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.title.lower() == other.title.lower()

    def __hash__(self):
        return hash(self.title.lower())


# аудиокнига это та же книга, только с длительностью, поэтому наследуюсь
# от Book и не копирую проверки. super() отдаёт родителю общие поля,
# а duration добавлен тут, потому что у обычной книги его нет
class AudioBook(Book):
    def __init__(self, title: str, author: str, year: int, duration: int):
        super().__init__(title, author, year)
        self.duration = duration

    # переопределил, потому что родительский from_data не знает про duration
    @classmethod
    def from_data(cls, data: dict):
        return cls(data["title"], data["author"], data["year"], data["duration"])

    # полиморфизм: метод называется так же как у Book, но вывод другой
    def get_info(self):
        return (f"Аудиокнига: «{self.title}», автор: {self.author}, "
                f"год: {self.year}, длительность: {self.duration} мин")


# линейный поиск: иду по списку по очереди и сравниваю названия.
# в худшем случае (книги нет или она последняя) проверяю все n книг,
# поэтому сложность O(n). для маленькой библиотеки этого хватает,
# бинарный поиск потребовал бы сортировки, что не окупится.
# счётчик checks возвращаю чтобы было видно сколько проверок сделано
def linear_search(books, title):
    checks = 0
    for book in books:
        checks += 1
        if book.title.lower() == title.strip().lower():
            return book, checks
    return None, checks


# класс для работы с бд, весь sql только тут, остальной код про sqlite
# ничего не знает. методы add/get_all/update/delete это CRUD.
# db_name можно передать, в тестах беру ":memory:" чтобы не трогать
# настоящий файл. duration не NOT NULL: у обычной книги там NULL,
# и по этому потом отличаю книгу от аудиокниги
class LibraryDB:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL,
                duration INTEGER
            )"""
        )
        self.conn.commit()

    # create. значения передаю через ? а не склеиваю строкой, так
    # безопаснее (sql-инъекции). getattr нужен потому что у Book нет
    # duration, тогда получится None
    @log_execution
    def add_book(self, book):
        duration = getattr(book, "duration", None)
        cur = self.conn.execute(
            "INSERT INTO books (title, author, year, duration) VALUES (?, ?, ?, ?)",
            (book.title, book.author, book.year, duration),
        )
        self.conn.commit()
        return cur.lastrowid

    # read. из бд приходят кортежи, превращаю их обратно в объекты.
    # возвращаю пары (id, книга), потому что id нужен для изменения и
    # удаления, а у самой книги такого поля нет
    @log_execution
    def get_all(self):
        rows = self.conn.execute(
            "SELECT id, title, author, year, duration FROM books ORDER BY id"
        ).fetchall()
        result = []
        for id_, title, author, year, duration in rows:
            data = {"title": title, "author": author, "year": year}
            if duration is None:
                result.append((id_, Book.from_data(data)))
            else:
                data["duration"] = duration
                result.append((id_, AudioBook.from_data(data)))
        return result

    # update и delete возвращают True/False: rowcount это сколько строк
    # затронуто, если 0 значит книги с таким id нет
    @log_execution
    def update_book(self, book_id, title, author, year, duration=None):
        cur = self.conn.execute(
            "UPDATE books SET title=?, author=?, year=?, duration=? WHERE id=?",
            (title, author, year, duration, book_id),
        )
        self.conn.commit()
        return cur.rowcount > 0

    @log_execution
    def delete_book(self, book_id):
        cur = self.conn.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()


# дальше консольное меню, оно только общается с пользователем

# без этой функции int(input()) падал бы на буквах, поэтому спрашиваю
# заново пока не введут число
def input_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


# собирает книгу или аудиокнигу из ввода. проверки тут не дублирую:
# если данные плохие, ValueError кидают сами классы, а я его ловлю
# и прошу ввести всё заново
def ask_book():
    while True:
        try:
            title = input("Название: ")
            author = input("Автор: ")
            year = input_int("Год выпуска: ")
            is_audio = input("Это аудиокнига? (д/н): ").strip().lower() == "д"
            if is_audio:
                return AudioBook(title, author, year, input_int("Длительность (мин): "))
            return Book(title, author, year)
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")


def show_books(db):
    books = db.get_all()
    if not books:
        print("Библиотека пуста.")
        return
    for id_, book in books:
        print(f"{id_}. {book}")


def main():
    db = LibraryDB()
    menu = (
        "\n=== Библиотека ===\n"
        "1. Добавить книгу\n"
        "2. Показать все книги\n"
        "3. Найти книгу по названию\n"
        "4. Изменить книгу\n"
        "5. Удалить книгу\n"
        "6. Экспорт книги в словарь (to_dict)\n"
        "0. Выход"
    )
    while True:
        print(menu)
        choice = input("Выбор: ").strip()
        if choice == "1":
            book = ask_book()
            print(f"Добавлено, id = {db.add_book(book)}")
        elif choice == "2":
            show_books(db)
        elif choice == "3":
            # поиск делаю своим linear_search по списку объектов, а не
            # sql-запросом, чтобы было видно O(n) и число проверок
            title = input("Название для поиска: ")
            books = [b for _, b in db.get_all()]
            found, checks = linear_search(books, title)
            print(found if found else "Книга не найдена.")
            print(f"Количество проверок: {checks} из {len(books)}")
        elif choice == "4":
            # сначала показываю список чтобы пользователь увидел id
            show_books(db)
            book_id = input_int("id книги для изменения: ")
            book = ask_book()
            ok = db.update_book(book_id, book.title, book.author, book.year,
                                getattr(book, "duration", None))
            print("Изменено." if ok else "Книга с таким id не найдена.")
        elif choice == "5":
            show_books(db)
            ok = db.delete_book(input_int("id книги для удаления: "))
            print("Удалено." if ok else "Книга с таким id не найдена.")
        elif choice == "6":
            # else у for сработает только если цикл не дошёл до break,
            # то есть книги с таким id нет
            show_books(db)
            book_id = input_int("id книги: ")
            for id_, book in db.get_all():
                if id_ == book_id:
                    print(book.to_dict())
                    break
            else:
                print("Книга не найдена.")
        elif choice == "0":
            db.close()
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню.")


# чтобы меню не запускалось при импорте (test_library.py импортирует main)
if __name__ == "__main__":
    main()
