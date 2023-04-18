from zad1.Librarian import Librarian
from zad1.Reader import Reader
from zad1.System import System

if __name__ == '__main__':
    sys = System()
    user = sys.login()
    sys.create_standard_context(user)
