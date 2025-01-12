from datetime import datetime

import sqlalchemy as sa
from enum import Enum
import sqlalchemy.orm as orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


# classes for defining different enum type
class RequestState(Enum):
    PENDING = 'pending'
    DENIED = 'denied'
    APPROVED = 'approved'


class RequestType(Enum):
    REPAIR = 'repair'
    TAKE = 'take'


class ItemState(Enum):
    NEW = 'new'
    USED = 'used'
    BROKEN = 'broken'


# SQLAlchemy models

# model for user roles (user or admin)
class Role(db.Model):
    __tablename__ = 'roles'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True, nullable=False)

    users = orm.relationship('User', back_populates='role')


# basic user model
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, unique=True, nullable=False)
    hashed_password = sa.Column(sa.String, nullable=False)
    role_id = sa.Column(sa.Integer, sa.ForeignKey('roles.id'), nullable=False, default=1)
    created_date = sa.Column(sa.DateTime, default=datetime.utcnow)

    role = orm.relationship('Role', back_populates='users')
    items = orm.relationship("Item", back_populates="user")
    requests = orm.relationship("Request", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


# model of inventory item
class Item(db.Model):
    __tablename__ = 'items'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    state = sa.Column(sa.Enum(ItemState), nullable=False, default=ItemState.NEW)
    quantity = sa.Column(sa.Integer, nullable=False)
    take_user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    requests = orm.relationship('Request', back_populates='item')
    user = orm.relationship('User', back_populates='items')


# model of request (for example request to repair item)
class Request(db.Model):
    __tablename__ = 'requests'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    item_id = sa.Column(sa.Integer, sa.ForeignKey('items.id'), nullable=False)
    state = sa.Column(sa.Enum(RequestState), default=RequestState.PENDING, nullable=False)
    type = sa.Column(sa.Enum(RequestType), default=RequestType.REPAIR, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)

    user = orm.relationship('User', back_populates='requests')
    item = orm.relationship('Item', back_populates='requests')

    @classmethod
    def create_request(cls, user_id, item_id, type):
        request = Request(user_id=user_id, item_id=item_id, type=type)
        db.session.add(request)
        db.session.commit()


# model for purchases
class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)
    supplier = sa.Column(sa.String, nullable=False)
    price = sa.Column(sa.Float, nullable=False)
    status = sa.Column(sa.Boolean(), nullable=False, default=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
