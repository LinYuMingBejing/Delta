from flask_script import Command

from app import db
from settings.defaults import SQLALCHEMY_DATABASE_URI

class ResetDBVersionCommand(Command):

    def run(self):
        """command run"""
        engine = db.create_engine(SQLALCHEMY_DATABASE_URI, {})
        db.engine.execute("drop table IF EXISTS alembic_version;")
