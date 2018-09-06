from collections import namedtuple
import traceback

from app.code.DBErrors import DBSQLError, DBCredentialsError, DBConnectionError, DBCommonError
from app.models.user import User
from app.models.task import Task
from app.models.tag import Tag
import datetime

DBFuncResult = namedtuple('DBFuncResult', 'result success err_msg err_obj')


def load_all_task_tags(db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load_tasks(db) -> DBFuncResult:
        _SQL = """select id, name from awards_types """
        db.exec_sql(_SQL, [])
        res = db.cursor.fetchall()

        if res:
            tags = []
            for tag in res:
                tags.append(Tag(id=tag[0], name=tag[1]))
            return DBFuncResult(tags, True, None, None)
        return DBFuncResult(None, False, "Не удалось получить список тэгов заданий", None)

    try:

        if db:
            return load_tasks(db)
        else:
            with db_use_class(db_config) as db:
                return load_tasks(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)



def load_category_name(category_id : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT name
        FROM awards_types
        WHERE id={category_id}
        """
        db.exec_sql(_SQL, [('category_id', category_id)])
        res = db.cursor.fetchall()

        if res:
            return DBFuncResult(res[0], True, None, None)
        return DBFuncResult(None, False, "Не удалось получить название категории", None)

    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


def add_award_request(id_user : int, id_award : int, letter, images : [], db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def add_request(db) -> DBFuncResult:
        _SQL = """
        INSERT INTO awards_requests(id_user, id_award, letter)
        VALUES({id_user}, {id_award}, {letter})
        returning id;
         """
        db.exec_sql(_SQL, [('id_user', id_user), ('id_award', id_award), ('letter', letter)])
        res = db.cursor.fetchall()

        if res:
            for src in images:
                req_add_requst_image = add_award_request_image(id_request_award=res[0], src=src, db=db)
                if not req_add_requst_image.success:
                    return DBFuncResult(None, False, str(req_add_requst_image.err_msg), req_add_requst_image.err_obj)
            return DBFuncResult(True, True, None, None)
        return DBFuncResult(None, False, "Не удалось отправить запрос наполучение награды", None)

    try:

        if db:
            return add_request(db)
        else:
            with db_use_class(db_config) as db:
                return add_request(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


def add_award_request_image(id_request_award : int, src : str, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def add_request(db) -> DBFuncResult:
        _SQL = """
        INSERT INTO requests_images(src, id_request_award)
        VALUES({src}, {id_request_award})
        returning id
         """
        db.exec_sql(_SQL, [('src', src), ('id_request_award', id_request_award)])
        res = db.cursor.fetchall()

        if res:
            return DBFuncResult(True, True, None, None)
        return DBFuncResult(None, False, "Не удалось отправить запрос наполучение награды", None)

    try:

        if db:
            return add_request(db)
        else:
            with db_use_class(db_config) as db:
                return add_request(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# создать пользователя
def create_user(surname : str, name : str, email : str, password_hash :str, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def create(db) -> DBFuncResult:
        _SQL = """
         INSERT INTO users(name, login, password_hash, is_admin, surname)
         VALUES({name}, {login}, {password_hash}, 0, {surname})
         returning id
         """
        db.exec_sql(_SQL, [('name', name), ('login', email), ('password_hash', password_hash), ('surname', surname)])
        res = db.cursor.fetchall()

        if res:
            return DBFuncResult(res[0], True, None, None)
        return DBFuncResult(None, False, "Не удалось создать пользовтеля", None)

    try:

        if db:
            return create(db)
        else:
            with db_use_class(db_config) as db:
                return create(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# загрузить пользователя по логину
def load_user_by_login(login : str, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
         SELECT id, name, login, password_hash, level, experience, coins, login_confirmed, is_admin, surname
         FROM users
         WHERE login={login}
         """
        db.exec_sql(_SQL, [('login', login)])
        res = db.cursor.fetchall()

        if res:
            return DBFuncResult(User(id=res[0][0], name=res[0][1], login = res[0][2], password_hash = res[0][3],
                                     level=res[0][4], experience=res[0][5], coins=res[0][6], login_confirmed=res[0][7],
                                     is_admin=res[0][8], surname=res[0][9]), True, None, None)
        return DBFuncResult(None, False, "Не удалось идентифицировать пользователя", None)

    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# загрузить пользователя по id
def load_user_by_id(user_id : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
         SELECT id, name, login, password_hash, level, experience, coins, login_confirmed, is_admin, surname
         FROM users
         WHERE id={id}
         """
        db.exec_sql(_SQL, [('id', user_id)])
        res = db.cursor.fetchall()

        if res:
            return DBFuncResult(User(id=res[0][0], name=res[0][1], login = res[0][2], password_hash = res[0][3],
                                     level=res[0][4], experience=res[0][5], coins=res[0][6], login_confirmed=res[0][7],
                                     is_admin=res[0][8], surname=res[0][9]), True, None, None)
        return DBFuncResult(None, False, "Не удалось идентифицировать пользователя", None)

    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


def system_user_update_properties(id_user: int, field_name__field_value_list: [],
                                      db_use_class=None, db_config=None, db=None) -> DBFuncResult:
        """Обновить данные пользователя в БД. Если задан парметр db, то SQL-команда отправляется через данное подключение
        к БД. db следует использовать в рамках "сложных" запросов, когда через db выполняется несколько запросов и
        после создания "персоны" может потребоваться "откат" (rollback) транзакции, открытой в рамках db
        :param id_user:
        :param field_name__field_value_list: Набор пар вида [поле - новое значение]: [('login_confirmed', 1), ('name', 'Новое название')]
        :param db_use_class:
        :param db_config:
        :param db:
        :return:
        """
        try:
            data = ("", [])

            for fname, fvalue in field_name__field_value_list:
                data = process_update_param_ex(fname, fvalue, data)

            update_fields = data[0]
            values_data = data[1]

            if update_fields:
                _SQL = """update users set """ + update_fields + """
                          where id = {id_user}
                          """

                values_data.append(('id_user', id_user))

                try:
                    if db is None:
                        with db_use_class(db_config) as db:
                            db.exec_sql(_SQL, values_data)
                    else:
                        db.exec_sql(_SQL, values_data)

                    return DBFuncResult(None, True, None, None)
                except DBCommonError as err:
                    return DBFuncResult(None, False, err.get_err_msg(), err)
            else:
                return DBFuncResult(None, False, 'Не задано ни одного поля', None)

        except Exception as err:
            return DBFuncResult(None, False, str(err), err)


def process_update_param_ex(field_name, field_value, data: tuple) -> tuple:
            """
            :param field_name: Название параметра
            :param field_value: Значение параметра.
            :param data: Кортеж, в котором первым элементом идёт список элементов вида "field_name={field_name}" , разделённые запятыми;
            вторым элементом - список кортежей вида (param_name, param_value)
            :return: Модифицированный кортеж data
            """""
            update_fields = data[0]
            values_data = data[1]

            if field_value:
                if update_fields:
                    update_fields = update_fields + ', ' + field_name + '={' + field_name + '}'
                else:
                    update_fields = field_name + '={' + field_name + '}'

                values_data.append((field_name, field_value))
            return update_fields, values_data


# получить все награды
def load_all_task(db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load_tasks(db) -> DBFuncResult:
        _SQL = """select id, name, id_award_type, coins, experience, requirement from awards """
        db.exec_sql(_SQL, [])
        res = db.cursor.fetchall()

        if len(res) > 0:
            awards = []
            for award in res:
                awards.append({'id' : award[0], 'name' : award[1], 'id_award_type' : award[2], 'coins' : award[3],
                               'experience' : award[4], 'requirement' : award[5]})
            return DBFuncResult(awards, True, None, None)
        else:
            return DBFuncResult([], False, "Не удалось получить список заданий", None)

    try:

        if db:
            return load_tasks(db)
        else:
            with db_use_class(db_config) as db:
                return load_tasks(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить все награды пользователя
def load_all_user_awards(user_id : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load_tasks(db) -> DBFuncResult:
        _SQL = """
        SELECT awards.name, awards.src
        FROM users_awards
        LEFT JOIN awards ON users_awards.id_award = awards.id
        WHERE users_awards.id_user={user_id}
         """
        db.exec_sql(_SQL, [('user_id', user_id)])
        res = db.cursor.fetchall()

        if len(res) > 0:
            awards = []
            for award in res:
                awards.append({'name' : award[0], 'src' : award[1]})
            return DBFuncResult(awards, True, None, None)
        else:
            return DBFuncResult([], False, "Не удалось получить список заданий", None)

    try:

        if db:
            return load_tasks(db)
        else:
            with db_use_class(db_config) as db:
                return load_tasks(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить все запросы пользователей
def load_all_requests(db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load_requests(db) -> DBFuncResult:
        _SQL = """
        SELECT awards_requests.id_award, awards.name, awards_requests.id_user, users.name, awards.requirement,
        awards_requests.letter, awards_requests.id
        FROM awards_requests
        LEFT JOIN awards ON awards_requests.id_award = awards.id
        LEFT JOIN users ON awards_requests.id_user = users.id
        """
        db.exec_sql(_SQL, [])
        res = db.cursor.fetchall()

        if len(res) > 0:
            requests = []
            for request in res:
                req_images = get_images_by_request_id(id_request=request[6], db=db)
                requests.append({'id_award' : request[0], 'award_name' : request[1], 'id_user' : request[2],
                                 'user_name' : request[3], 'requirement' : request[4], 'letter' :request[5],
                                 'id' : request[6], 'images' : req_images.result})
            return DBFuncResult(requests, True, None, None)
        else:
            return DBFuncResult([], False, "Не удалось получить список заданий", None)

    try:

        if db:
            return load_requests(db)
        else:
            with db_use_class(db_config) as db:
                return load_requests(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить награды по жанру
def load_all_task_by_category(category : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load_tasks(db) -> DBFuncResult:
        _SQL = """
        SELECT id, name, id_award_type, coins, experience, requirement, src
        FROM awards
        WHERE id_award_type={category}
         """
        db.exec_sql(_SQL, [('category', category)])
        res = db.cursor.fetchall()

        if len(res) > 0:
            awards = []
            for award in res:
                awards.append({'id' : award[0], 'name' : award[1], 'id_award_type' : award[2], 'coins' : award[3],
                               'experience' : award[4], 'requirement' : award[5], 'src' : award[6]})
            return DBFuncResult(awards, True, None, None)
        else:
            return DBFuncResult([], False, "Не удалось получить список заданий", None)

    try:

        if db:
            return load_tasks(db)
        else:
            with db_use_class(db_config) as db:
                return load_tasks(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# создать награду
def create_award(name : str, requirement : str, coins : int, experience : int, id_award_type, image_src : str, db_use_class=None,
                 db_config=None, db=None) -> DBFuncResult:

    def create(db) -> DBFuncResult:
        _SQL = """
        INSERT INTO awards(name, requirement, coins, experience, id_award_type, src)
        VALUES ({name},{requirement},{coins},{experience},{id_award_type}, {src})
        returning id
        """
        db.exec_sql(_SQL, [('name', name), ('requirement', requirement), ('coins', int(coins)), ('experience', int(experience)),
                           ('id_award_type', int(id_award_type)), ('src', image_src)])
        res = db.cursor.fetchall()

        if not res:
            return DBFuncResult(None, False, 'Не удалось загрузить награду', None)

        res_get_award = get_award_by_id(id_award=res[0], db=db)

        return DBFuncResult(res_get_award.result, True, None, None)

    try:

        if db:
            return create(db)
        else:
            with db_use_class(db_config) as db:
                return create(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить награду по id
def get_award_by_id(id_award : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT id, name, requirement, coins, experience, id_award_type, src
        FROM awards
        WHERE id={id}
        """
        db.exec_sql(_SQL, [('id', id_award)])
        res = db.cursor.fetchall()

        if len(res) > 0:
            return DBFuncResult({'id' : res[0][0], 'name' : res[0][1], 'requirement' : res[0][2], 'coins' : res[0][3],
                               'experience' : res[0][4], 'id_award_type' : res[0][5], 'src' : res[0][6] }, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось загрузить награду", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить награду по id запроса
def get_images_by_request_id(id_request : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT src
        FROM requests_images
        WHERE id_request_award={id_request}
        """
        db.exec_sql(_SQL, [('id_request', id_request)])
        res = db.cursor.fetchall()

        if len(res) > 0:
            return DBFuncResult(res, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось загрузить награду", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# нагрдадить пользователя
def reward(id_user : int, id_award : int, id_request : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:
    def reward_user(db) -> DBFuncResult:
        _SQL = """
        UPDATE users
        SET coins={coins}, experience={experience}
        WHERE id={id_user}
        returning id;
        """
        _SQL_ADD_AWARD="""
        INSERT INTO users_awards(id_user, id_award)
        VALUES({id_user}, {id_award})
        """
        _SQL_REMOVE_REQUEST="""
        DELETE FROM awards_requests
        WHERE id={id_request}
        returning id;
        """
        req_award = get_award_by_id(id_award=id_award, db=db)
        req_images = get_images_by_request_id(id_request=id_request, db=db)
        if not req_award.success:
            return DBFuncResult(None, False, req_award.err_msg, None)

        req_user = load_user_by_id(user_id=id_user, db=db)

        if not req_user.success:
            return DBFuncResult(None, False, req_user.err_msg, None)

        db.exec_sql(_SQL_ADD_AWARD, [('id_user', id_user), ('id_award', id_award)])

        db.exec_sql(_SQL, [('id_user', id_user), ('coins', req_award.result['coins']+req_user.result.coins),
                           ('experience', req_award.result['experience'] + req_user.result.experience)])

        db.exec_sql(_SQL_REMOVE_REQUEST, [('id_request', id_request)])

        res = db.cursor.fetchall()

        if len(res) > 0:
            req_add_news = add_news(id_user=id_user, id_award=id_award, images=req_images.result, db=db)
            if not req_add_news.success:
                return DBFuncResult(None, False, req_add_news.err_msg, None)

            return DBFuncResult(True, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось наградить пользователя", None)
    try:

        if db:
            return reward_user(db)
        else:
            with db_use_class(db_config) as db:
                return reward_user(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить pg_equipment
def get_pg_equipment(db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT *
        FROM users
        """
        db.exec_sql(_SQL, [])
        res = db.cursor.fetchall()

        if len(res) > 0:
            return DBFuncResult(res, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось загрузить pg_equipment", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# удалить награду
def delete_award(id_award: int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        DELETE FROM awards
        WHERE id={id_award}
        returning id
        """
        db.exec_sql(_SQL, [('id_award', id_award)])
        res = db.cursor.fetchall()

        if len(res) > 0:
            return DBFuncResult(True, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось удалить награду", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# добавить новость
def add_news(id_user : int, id_award: int, images : [],
                db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def add(db) -> DBFuncResult:
        _SQL = """
        INSERT INTO news(id_user, id_award, date)
        VALUES({id_user}, {id_award}, {date})
        returning id
        """

        _SQL_ADD_IMAGES = """
        INSERT INTO news_images(id_new, src)
        VALUES({id_new}, {src})
        returning id
        """

        db.exec_sql(_SQL, [('id_award', id_award), ('id_user', id_user), ('date', datetime.datetime.now())])
        res = db.cursor.fetchall()

        if not res or len(res) == 0:
            return DBFuncResult(None, False, "Не удалось создать новость", None)

        for i in images:
            db.exec_sql(_SQL_ADD_IMAGES, [('id_new', res), ('src', i)])
            res = db.cursor.fetchall()
            if not res or len(res) == 0:
                return DBFuncResult(None, False, "Не удалось прикрепить фотку к новости", None)

        return DBFucnResult(True, True, None, None)


    try:

        if db:
            return add(db)
        else:
            with db_use_class(db_config) as db:
                return add(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить новость начиная с
def load_news_from(id_first : int, db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT n.id, awards.name, users.name, users.id
        FROM news n
        LEFT JOIN awards ON n.id_award = awards.id
        LEFT JOIN users ON n.id_user = users.id
        WHERE id BETWEEN {id_first} and {id_second}
        ORDER BY date DESC;
        """
        db.exec_sql(_SQL, [('id_first', id_first), ('id_second', id_first-10)])
        res = db.cursor.fetchall()
        news = []
        if len(res) > 0:
            for n in res:
                news.append({'id' : n[0], 'award_name' : n[1],
                    'user_name' : n[2], 'user_id' : n[3]}, True, None, None)
            return DBFuncResult(news, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось получить новости", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить первые последний 10 новостей
def load_news(db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT n.id, awards.requirement, users.name, users.id
        FROM news n
        LEFT JOIN awards ON n.id_award = awards.id
        LEFT JOIN users ON n.id_user = users.id
        ORDER BY date DESC
        limit 10;
        """
        db.exec_sql(_SQL, [])
        res = db.cursor.fetchall()
        news = []
        if len(res) > 0:
            for n in res:
                news.append({'id' : n[0], 'award_requirement' : n[1],
                    'user_name' : n[2], 'user_id' : n[3]})
            return DBFuncResult(news, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось получить новости", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)


# получить лучших 10 пользователей
def load_best_users(db_use_class=None, db_config=None, db=None) -> DBFuncResult:

    def load(db) -> DBFuncResult:
        _SQL = """
        SELECT id, name, experience
        FROM users
        ORDER BY experience DESC
        limit 10;
        """
        db.exec_sql(_SQL, [])
        res = db.cursor.fetchall()
        users = []
        if len(res) > 0:
            for u in res:
                users.append({'id' : u[0], 'name' : u[1],
                    'experience' : u[2]})
            return DBFuncResult(users, True, None, None)
        else:
            return DBFuncResult(None, False, "Не удалось получить лучших пользователей", None)
    try:

        if db:
            return load(db)
        else:
            with db_use_class(db_config) as db:
                return load(db)

    except DBCommonError as err:
        return DBFuncResult(None, False, err.get_err_msg(), err)
    except Exception as err:
        return DBFuncResult(None, False, str(err), err)

