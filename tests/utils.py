import os

from sqlalchemy import BigInteger, Column, MetaData, Table, Text

from flask_sqlalchemy_core import FlaskSQLAlchemy

db = FlaskSQLAlchemy(os.environ['DATABASE_URL'])

metadata = MetaData()


NotesTable = Table(
    'notes', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('name', Text, unique=True, nullable=False),
    Column('text', Text),
)
