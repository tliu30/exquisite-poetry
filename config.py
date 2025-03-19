import os


class Config:
    APP_NAME = "exquisite-poetry"
    FLASK_MIGRATE_DIRECTORY = "./migrations"
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
    SERVER_NAME = os.environ.get("SERVER_NAME", "127.0.0.1:5000")
    GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
    GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")


config = Config()
