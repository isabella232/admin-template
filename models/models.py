import app_config

from peewee import Model, PostgresqlDatabase
from peewee import BooleanField, CharField, DateField, DateTimeField, DecimalField, ForeignKeyField, IntegerField
from slugify import slugify
from playhouse.postgres_ext import JSONField

import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.WARNING)
logger.addHandler(logging.StreamHandler())

db = PostgresqlDatabase(
    app_config.DATABASE['PGDATABASE'],
    user=app_config.DATABASE['PGUSER'],
    password=app_config.DATABASE['PGPASSWORD'],
    host=app_config.DATABASE['PGHOST'],
    port=app_config.DATABASE['PGPORT']
)

class BaseModel(Model):
    """
    Base class for Peewee models. Ensures they all live in the same database.
    """
    class Meta:
        database = db

class TestModel(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()
    birthday = DateField()
    ranking = IntegerField()