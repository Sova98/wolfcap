from app.code.DBcm import UseDatabase
from app.config import Config

db_config =  Config.DB_CONFIG #{'dbname': 'aschool', 'user': 'postgres', 'password': 'admin', 'host': '127.0.0.1'}
db_use_class = UseDatabase