from utils import manage_context, get_data
from Librarian import Librarian
from Reader import Reader
from Constants import READER_DB, LIBRARIAN_DB


class System:
    READER_DB = READER_DB
    LIBRARIAN_DB = LIBRARIAN_DB

    def login(self):
        print("Welcome to our library!")
        print("As who do you want to login?:")
        user_type = manage_context(["Reader", "Librarian"])
        match user_type:
            case 'Librarian':
                return Librarian(self.validate_credentials(self.LIBRARIAN_DB))
            case 'Reader':
                return Reader(self.validate_credentials(self.READER_DB))

    def create_standard_context(self, user) -> None:
        context = user.standard_context
        while True:
            choice: str = manage_context(list(context.keys()))
            if choice == "Return":
                break
            context[choice]()

    def validate_credentials(self, db_path: str) -> dict[str,]:
        while True:
            try:
                print("Enter credentials!")
                email = input("email: ")
                password = input("password: ")
                data = get_data(db_path)
                users = data["users"]
                if users[email]["password"] == password:
                    return {"email": email} | users[email]
                else:
                    raise KeyError
            except KeyError:
                print("Email or password incorrect!")
