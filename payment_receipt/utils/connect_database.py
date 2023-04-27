import psycopg2
from dotenv import find_dotenv, dotenv_values
import pyodbc
from payment_receipt import const


class DatabaseConnect:

    def __init__(self):
        self.env = {**dotenv_values(dotenv_path=find_dotenv())}

    def connection(self):

        cnx = pyodbc.connect(f'{self.env["DO_DB_DRIVER"]};{self.env["DO_DB_HOST"]};'
                             f'{self.env["DO_DB_SERVER"]};{self.env["DO_DB_USER"]};'
                             f'{self.env["DO_DB_PWD"]};')

        cursor = cnx.cursor()

        return cursor

    def return_consult(self, query):
        result = self.connection().execute(query)
        return result

    @staticmethod
    def connect_rds():

        try:
            engine = psycopg2.connect(
                database=const.DATABASE,
                user=const.USER,
                password=const.PWD,
                host=const.HOST,
                port=const.PORT)

            cursor = engine.cursor()

            return cursor

        except Exception:
            pass