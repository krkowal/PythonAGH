class User:
    def __init__(self, user_data, context):
        self.email = user_data["email"]
        self.password = user_data["password"]
        self.STANDARD_CONTEXT = context
        self.STANDARD_CONTEXT["View catalog"] = self.view_catalog

    def view_catalog(self):
        print("view catalog loop")
