from zad1.User import User


class Reader(User):
    def __init__(self, user_data):
        super().__init__(user_data)
        self.borrowed_books = user_data["borrowed_books"]

    def __str__(self):
        return f"Reader\nEmail: {self.email}\nPassword: {self.password}\nBorrowed books: {self.borrowed_books}"

# TODO wypożyczenie książki
# TODO zarezerwowanie ksiązki, która jest wypożyczona
# TODO przedłużanie wypożyczenia
# TODO przeglądanie katalogu
