class DBCommonError(Exception):
    """" Класс ошибки при работе с БД """

    def get_err_msg(self) -> str:
        msg = str(self)
        if msg is None or msg == '':
            return str(self.__class__)
        else:
            return msg


class DBConnectionError(DBCommonError):
    """" Класс ошибки подключения к БД """
    pass


class DBCredentialsError(DBCommonError):
    """" Класс ошибки подключения к БД """
    pass


class DBSQLError(DBCommonError):
    """" Класс ошибки при выполнении запроса к БД """
    pass
