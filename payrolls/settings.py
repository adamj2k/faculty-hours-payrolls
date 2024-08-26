import os

from dotenv import load_dotenv

load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE")
DB_HOST = os.getenv("DB_HOST")
DB_DB = os.getenv("DB_DB")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
SQLALCHEMY_DATABASE_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
FH_APP_FACULTY_URL = os.getenv("FH_APP_FACULTY_URL")
FH_APP_REPORT_URL = os.getenv("FH_APP_REPORT_URL")
