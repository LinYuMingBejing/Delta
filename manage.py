import app
from app import db
from cmd.reset_db_cmd import ResetDBVersionCommand

from flask_migrate import Migrate, MigrateCommand
import flask_script as script

app = app.create_application()

manager = script.Manager(app)
manager.add_command('reset-db-version', ResetDBVersionCommand)
migrate = Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand)

if __name__=="__main__":
    manager.run()
