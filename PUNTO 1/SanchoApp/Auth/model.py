



from datetime import datetime
from flask_login import UserMixin  # used to manage the login state inside the db
from sqlalchemy.orm import relationship
from SanchoApp import db
from SanchoApp.Clients.controller import DEFAULT_USER_PICTURE_STATIC_PATH


class User(UserMixin, db.Model):

    __tablename__="usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default=DEFAULT_USER_PICTURE_STATIC_PATH)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


def create_new_user(**kargs) -> type(User):
    new_user = User(
        username=kargs["username"],
        password=kargs["password"],
        email= kargs["email"] if "email" in kargs else None,
        image_file=kargs["image_file"] if "image_file" in kargs else None
    )
    db.session.add(new_user)
    db.session.commit()

    return new_user
