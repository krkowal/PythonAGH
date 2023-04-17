class Book:
    def __init__(self, title: str, author: str, key_words: list[str]):
        self.title = title
        self.author = author
        self.key_words = key_words

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Key words: {self.key_words}"
