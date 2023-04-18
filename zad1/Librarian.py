from zad1.User import User


class Librarian(User):
    def __init__(self, user_data):
        context = {
            "Take in return": self.take_in_return,
            "Add new book": self.add_new_book,
            "Remove book": self.remove_book,
            "Add new reader": self.add_reader,
        }
        super().__init__(user_data, context)

    def __str__(self):
        return f"Librarian\nEmail: {self.email}\nPassword: {self.password}"

    def take_in_return(self):
        print("take in book return loop")

    def add_new_book(self):
        print("add new book loop")

    def remove_book(self):
        print("remove book loop")

    def add_reader(self):
        print("add reader loop")

# context -> take in return, add new book, remove book, add reader, view catalog
# take in return -> user_email and book_id
# add new book -> book data
# remove book -> book_id
# add reader -> reader data
# view catalog -> books -> see if book is borrowed and who borrowed it and when it is available
