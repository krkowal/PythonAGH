from zad1.User import User


class Librarian(User):
    def __init__(self, user_data):
        super().__init__(user_data)

    def __str__(self):
        return f"Librarian\nEmail: {self.email}\nPassword: {self.password}"
