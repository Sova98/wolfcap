import psycopg2, psycopg2.extensions
from app.code.DBErrors import DBConnectionError, DBCredentialsError, DBSQLError, DBCommonError


# conf = {'dbname':'aschool', 'user':'postgres', 'password':'admin', 'host':'127.0.0.1'}

class UseDatabase:
    def __init__(self, config):
        self.config = config
        self.paramstyle = psycopg2.paramstyle

    def __enter__(self) -> 'UseDatabase':
        try:
            self.connection = psycopg2.connect(**self.config)
            self.cursor = self.connection.cursor()
            return self

        except psycopg2.OperationalError as err:
            raise DBConnectionError(err)
        except psycopg2.InterfaceError as err:
            raise DBConnectionError(err)
        except psycopg2.ProgrammingError as err:
            raise DBCredentialsError(err)
        except psycopg2.DatabaseError as err:
            raise DBCommonError(err)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type:
                self.connection.commit()
            else:
                self.connection.roleback()
            self.cursor.close()
            self.connection.close()
        except psycopg2.ProgrammingError as err:
            raise DBSQLError(exc_val)
        except psycopg2.DatabaseError as err:
            raise DBCommonError(exc_val)
        except psycopg2.Error as err:
            raise DBCommonError(exc_val)

        if exc_type is psycopg2.ProgrammingError:
            raise DBSQLError(exc_val)
        elif exc_type is psycopg2.Error:
            raise DBCommonError(exc_val)
        elif exc_type is psycopg2.IntegrityError:
            raise DBCommonError(exc_val)
        elif exc_type:
            raise exc_type(exc_val)

    def exec_sql(self, sql: str, params: []) -> str:
        """" Метод выполняет SQL с корректной передачей параметров методу execute
        Параметры передаются в виде: [(id, value_of_id), (name, value_of_name), ...]
        В SQL параметры задаются в виде: "select * from users where id={id} and name={name}"
        """
        ph = None

        if self.paramstyle == 'qmark':
            ph = "?"
        elif self.paramstyle == 'format':
            ph = "%s"

        for k, _ in params:
            if not k or not k.isidentifier():
                raise DBSQLError("Некорректный идентификатор: {}".format(k))

        if ph:
            values = []
            for k, v in params:
                sql = sql.replace("{" + str(k) + "}", ph)
                values.append(v)

            self.cursor.execute(sql, values)
        elif self.paramstyle == 'pyformat':
            values = {}
            for param in params:
                sql = sql.replace("{" + str(param[0]) + "}", "%(" + str(param[0]) + ")s")
                values[param[0]] = param[1]

            self.cursor.execute(sql, values)
        else:
            raise DBSQLError("Не поддерживается запрос с подстановками в виде: {}".format(self.paramstyle))
