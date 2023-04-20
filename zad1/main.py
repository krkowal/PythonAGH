from zad1.System import System

if __name__ == '__main__':
    sys = System()
    user = sys.login()
    sys.create_standard_context(user)
