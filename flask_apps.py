
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///database.db')

#engine = create_engine('sqlite:///database.db')

db = SQLAlchemy(app)
#db = sqlalchemy(app)
#db.metadata.reflect(engine)