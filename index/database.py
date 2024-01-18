from src.Entity import *
from sqlalchemy import create_engine
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Database(metaclass=SingletonMeta):
    # Base class for our models
    Base = declarative_base()

    def __init__(self):
        """
        Initializes the database engine.
        """
        DATABASE_URL = "sqlite:///base.db"

        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)()

    def get_session(self):
        """
        Provides a new session for database operations.
        :return: A new SQLAlchemy session
        """
        return self.Session

    def create_tables(self):
        """
        Creates tables in the database based on defined models.
        """
        self.Base.metadata.create_all(self.engine)
