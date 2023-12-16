from src.Entity import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Bootstrap():
    def bootstrap(self):
        DATABASE_URL = "sqlite:///base.db"
        engine = create_engine(DATABASE_URL, echo=True)

        Base.metadata.create_all(bind=engine)

        engine.dispose()
