
from flask.cli import FlaskGroup
from app import app
from extensions import db
from models import *

cli = FlaskGroup(app)

if __name__ == '__main__':
    cli()
