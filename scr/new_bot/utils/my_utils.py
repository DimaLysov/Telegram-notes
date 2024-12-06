class Person:
    def __init__(self, user_name: str, chat_id: int | None, name: str, surname: str | None):
        self.user_name = user_name
        self.chat_id = chat_id
        self.name = name.lower()
        if surname is None:
            self.surname = surname
        else:
            self.surname = surname.lower()
