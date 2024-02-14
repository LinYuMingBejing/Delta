import app
from app import db
from flask_migrate import Migrate, MigrateCommand
import flask_script as script

app = app.create_application()

manager = script.Manager(app)
migrate = Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand)

if __name__=="__main__":
    manager.run()
