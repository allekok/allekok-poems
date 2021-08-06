import logging
import sys
import os

try:
    from peewee import (Model,
                        SqliteDatabase,
                        CharField,
                        IntegerField,
                        TextField,
                        ForeignKeyField)

except ModuleNotFoundError as e:
    print("Install requirements by running ``pip install -r requirements.txt`` in your virtual environment.")
    sys.exit(f"Due missing required package, {e.args[0]}")

logger = logging.getLogger(__name__)

# Change the connection type for other SQL-Based DBs if wanted.
DB_NAME = 'allekok.db'
db = SqliteDatabase(DB_NAME)


class BaseModel(Model):
    class Meta:
        database = db


class PoetModel(BaseModel):
    full_name = CharField()
    view = IntegerField(default=0)
    surname = CharField()
    name = CharField()
    description = TextField(null=True)


class BookModel(BaseModel):
    name = CharField()
    view = IntegerField(default=0)
    poet_id = ForeignKeyField(PoetModel, backref='books')


class PoemModel(BaseModel):
    name = CharField()
    text = TextField()
    description = TextField(null=True)
    lang = CharField(null=True)
    tag = CharField(null=True)
    link = CharField(null=True)
    view = IntegerField(default=0)
    book_id = ForeignKeyField(BookModel, backref='poems')


def create_tables() -> None:
    logger.info("Create new database.")
    logger.info('Invoke create tables.')
    db.create_tables([BookModel,
                      PoetModel,
                      PoemModel])
    logger.info('Tables created.')


def remove_database() -> None:
    logger.info("Removing previous database.")
    try:
        os.remove(DB_NAME)
        logger.info("Database removed.")
    except FileNotFoundError:
        logger.info("DB not found, probably already deleted")
