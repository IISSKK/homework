class Book: 
    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self):
        return f"Книга: {self.title} Автор: {self.author} Страниц: {self.pages}"

    def __repr__(self):
        return f"Книга: (title='{self.title}', Автор='{self.author}', Страница='{self.pages}')"

    def __add_(self, other):
        if isinstance(other, Book):
            return self.pages + other.pages
        return False

    def __eq__(self, other):
        if isinstance(other, Book):
            return self.pages == other.pages
        return False

book1 = Book(title='<<Python Crash Course>>', author='Eric Matthes', pages=554)
book2 = Book(title='<<Clean Code>>', author='Robert C. Martin', pages=464)
book3 = Book(title='<<Fluent Python>>', author='Luciano Ramalho', pages=1000)

print('--- Проверка метода __str__ ---')
print(book1)
print(book2)

print('\n--- Проверка метода __repr__ ---')
print(repr(book1))
print([book1, book2,book3])

print('\n--- Проверка метода __add__ ---')
total_pages = book1 =book2
print(f'Сумма страниц book1 + book2 = {total_pages}')

print('\n--- Проверка метода __eq__ ---')
book4 = Book(title='Another Book', author='Unknown', pages=544)
print(f'book1 == book4 (Одинаковое кол-во страниц?): {book1 == book4}')
print(f'book1 == book2 (Разное кол-во страниц?): {book1 == book2}')