"""Models for Blogly."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.app_context().push()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):

    __tablename__ =  'users'

    with app.app_context():
        db.create_all   

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True, default='https://png.pngitem.com/pimgs/s/508-5087236_tab-profile-f-user-icon-white-fill-hd.png')

    
    


    
