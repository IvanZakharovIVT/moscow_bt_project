class UserAuthorizationError(Exception):
    def __init__(self, username: str):
        self.username = username

    @property
    def error_message(self) -> str:
        return "Неверно указан логин или пароль"


class UserValidateFieldError(Exception):
    action_name: str

    def __init__(self, user_type: str):
        self.user_type = user_type

    @property
    def error_message(self) -> str:
        return (f"Ошибка {self.action_name} пользователя. Для пользователя типа {self.user_type.description}"
                f" указаны не все поля")


class UserPermissionError(Exception):
    def __init__(self, username: str):
        self.username = username

    @property
    def error_message(self) -> str:
        return f"Ошибка доступа для {self.username}. Недостаточно прав"


class UserUniqueUsernameError(UserValidateFieldError):
    def __init__(self, username: str):
        self.username = username

    @property
    def error_message(self) -> str:
        return f"Ошибка создания пользователя. Пользователь с логином {self.user_type} уже существует"
