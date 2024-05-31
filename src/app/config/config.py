# config.py

# config/config.py
class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "cafenova"
}
