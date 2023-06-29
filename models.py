"""Models for Blogly."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.app_context().push()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

DEFAULT_IMG_URL = 'https://png.pngitem.com/pimgs/s/508-5087236_tab-profile-f-user-icon-white-fill-hd.png'
class User(db.Model):

    __tablename__ =  'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=True, default=DEFAULT_IMG_URL)
    posts = db.relationship('Post',back_populates="user")
    print(image_url)
    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} {self.image_url} >"
    
class Post(db.Model):
    """Post Model"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable = False)
    create_at = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False) ##tablename.fieldname makes PK/FK relationship

    user = db.relationship('User', back_populates="posts")
    
    @property
    def friendly_date(self):
        """Return to a nicely-formatted date."""

        return self.create_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    def __repr__(self):
        return f"<Post {self.title} {self.content} {self.create_at} {self.user_id}>"


