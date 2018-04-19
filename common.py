from config import Config
import psycopg2
import psycopg2.extras
import hashlib
import os
import urllib


def open_database():
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print(exception)
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value
    return wrapper


@connection_handler
def query_handler(cursor, querystring, *args, **kwargs):
    cursor.execute(querystring, *args, **kwargs)
    try:
        result = cursor.fetchall()
        return result
    except:
        pass


def hash_password(password):
    # Hash and salt password
    password_bytes = password.encode('utf-8')
    salt = 'ulezshgdxksaeurbcaskje'
    salt_bytes = salt.encode('utf-8')
    hashed_password = hashlib.sha512(password_bytes + salt_bytes).hexdigest()
    return hashed_password


def user_select():
    return query_handler("""SELECT * FROM users;""")


def add_user(username, password):
    return query_handler("""INSERT INTO users(username, password)
                         VALUES(%s, %s);""",
                         (username, password))


def get_user(username, password):
    return query_handler("""SELECT id, username FROM users
                         WHERE username = %(username)s and password = %(password)s;""",
                         {'username': username, 'password': password})