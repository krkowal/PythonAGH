from zad1.Librarian import Librarian
from zad1.Reader import Reader
from zad1.System import System

if __name__ == '__main__':
    sys = System()
    user = sys.login()
    if isinstance(user, Reader):
        sys.reader_context(user)
    elif isinstance(user, Librarian):
        sys.librarian_context(user)
