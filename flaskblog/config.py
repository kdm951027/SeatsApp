import os

class Config:
    SECRET_KEY = 'a13695295bf263db50f3481d0d63bddc'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # DATA_BACKEND = 'cloudsql'
    # PROJECT_ID = '	spot-254301'
    # CLOUDSQL_USER = 'root'
    # CLOUDSQL_PASSWORD = 'asdD1313'
    # CLOUDSQL_DATABASE = 'spot_db'
    #
    # CLOUDSQL_CONNECTION_NAME = 'spot-254301:us-central1:spot-sql-instance'
    #
    # # Alternatively, you could use a local MySQL instance for testing.
    # LOCAL_SQLALCHEMY_DATABASE_URI = (
    #     'mysql+pymysql://{user}:{password}@127.0.0.1:3307/{database}').format(
    #         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
    #         database=CLOUDSQL_DATABASE)
    #
    # # When running on App Engine a unix socket is used to connect to the cloudsql
    # # instance.
    # LIVE_SQLALCHEMY_DATABASE_URI = (
    #     'mysql+pymysql://{user}:{password}@localhost/{database}'
    #     '?unix_socket=/cloudsql/{connection_name}').format(
    #         user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
    #         database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)
    #
    # # SQLALCHEMY_DATABASE_URI = (
    # #     'mysql+pymysql://root:asdD1313@/bookshelf?unix_socket=/cloudsql/tutorial-254123:us-central1:bookshelf-db'
    # # )
    #
    # #
    # if os.environ.get('GAE_INSTANCE'):
    #     SQLALCHEMY_DATABASE_URI = LIVE_SQLALCHEMY_DATABASE_URI
    # else:
    #     SQLALCHEMY_DATABASE_URI = LOCAL_SQLALCHEMY_DATABASE_URI
