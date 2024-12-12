class Person:
    def __init__(self, user_name: str, chat_id: int | None, name: str, surname: str | None):
        if user_name[0] == '@':
            self.user_name: str = user_name
        else:
            self.user_name: str = '@' + user_name
        self.chat_id: int | None = chat_id
        self.name: str = name.lower()
        if surname is None:
            self.surname: None = surname
        else:
            self.surname: str = surname.lower()
