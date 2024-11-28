import datetime
import enum
from enum import Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from cProfile import label
from email.policy import default
from pickle import TRUE

from sqlalchemy.sql import func
from sqlalchemy.sql import expression
from sqlalchemy.sql import text

from config.db import db



# class BookMetadata(db.Model):
#     __tablename__ = 'dg_book_metadata'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('dg_book.id'))
#     isbn = db.Column(db.String(13))
#     language = db.Column(db.String(10))
#     cover_image = db.Column(db.String(255))
#     physical_location = db.Column(db.String(50))
#     qr_code = db.Column(db.String(255))
#     edition = db.Column(db.String(50))
#     publisher = db.Column(db.String(100))
#     pages = db.Column(db.Integer)
#     publication_date = db.Column(db.Date)
#     book = db.relationship('dg_book', backref='metadata', lazy=True)
    

# class BookCondition(db.Model):
#     __tablename__ = 'dg_book_condition'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('dg_book.id'))
#     condition_status = db.Column(db.Enum('new', 'good', 'fair', 'poor'))
#     last_inspection_date = db.Column(db.DateTime)
#     damage_notes = db.Column(db.Text)
#     maintenance_history = db.Column(db.JSON)
#     book = db.relationship('dg_book', backref='condition', lazy=True)
    

# class LoanReminder(db.Model):
#     __tablename__ = 'dg_loan_reminder'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     loan_id = db.Column(db.Integer, db.ForeignKey('dg_loan.id'))
#     reminder_date = db.Column(db.DateTime)
#     reminder_type = db.Column(db.Enum('upcoming_due', 'overdue', 'return_confirmation'))
#     sent_status = db.Column(db.Boolean, default=False)
#     reminder_message = db.Column(db.Text)
#     loan = db.relationship('dg_loan', backref='reminders', lazy=True)
    

# class Fine(db.Model):
#     __tablename__ = 'dg_fine'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     loan_id = db.Column(db.Integer, db.ForeignKey('dg_loan.id'))
#     amount = db.Column(db.Decimal(10, 2))
#     reason = db.Column(db.String(100))
#     status = db.Column(db.Enum('pending', 'paid', 'waived'))
#     payment_date = db.Column(db.DateTime)
#     loan = db.relationship('dg_loan', backref='fines', lazy=True)
    

# class ArticleMetrics(db.Model):
#     __tablename__ = 'dg_article_metrics'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     article_id = db.Column(db.Integer, db.ForeignKey('dg_article.id'))
#     views = db.Column(db.Integer, default=0)
#     downloads = db.Column(db.Integer, default=0)
#     citations = db.Column(db.Integer, default=0)
#     last_updated = db.Column(db.DateTime, default=func.now())
    
#     article = db.relationship('dg_article', backref='metrics', lazy=True)
    

# class ArticleKeyword(db.Model):
#     __tablename__ = 'dg_article_keyword'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     article_id = db.Column(db.Integer, db.ForeignKey('dg_article.id'))
#     keyword = db.Column(db.String(50))

# class ArticleCoAuthor(db.Model):
#     __tablename__ = 'dg_article_coauthor'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     article_id = db.Column(db.Integer, db.ForeignKey('dg_article.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('dg_users.id'))
#     contribution_type = db.Column(db.String(50))
#     order = db.Column(db.Integer)

# class Notification(db.Model):
#     __tablename__ = 'dg_notification'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('dg_users.id'))
#     type = db.Column(db.String(50))
#     message = db.Column(db.Text)
#     read = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=func.now())
#     updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())


# class dg_users_future(db.Model):
#     __tablename__ = 'dg_users_future'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     u_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
#     u_username = db.Column(db.String(128), unique=True, nullable=False)
#     u_name = db.Column(db.String(128))
#     u_firstname = db.Column(db.String(128))
#     u_lastname = db.Column(db.String(128))
#     u_email = db.Column(db.String(100), unique=True, nullable=False)
#     u_password_hash = db.Column(db.String(255), nullable=False)

#     # Future fields for user profile
#     u_mobile = db.Column(db.String(15), nullable=True)
#     u_address = db.Column(db.String(128), nullable=True)
#     u_country = db.Column(db.String(128), nullable=True)
#     u_city = db.Column(db.String(128), nullable=True)
#     u_first_login = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)

#     # Future fields related to education and function
#     role = db.Column(db.Enum('admin', 'user', 'studient', name='user_roles'), default='user')
#     field_of_study = db.Column(db.String(100))
#     education_leve = db.Column(db.Enum('professor', 'doctor', 'master', 'licence', 'bts', 'bt', 'bac', name='education_level'), default='bac')
#     function = db.Column(db.Enum('professor', 'doctor'))
#     u_status = db.Column(db.Enum(UserStatus), default=UserStatus.ACTIVE.name)

#     # Future functionality for storing user image
#     u_image_link = db.Column(db.Text())

#     created_at = db.Column(db.DateTime, default=func.now())
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# class dg_categories(db.Model):
#     __tablename__ = 'dg_categories'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     cat_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
#     cat_label = db.Column(db.String(128))
#     cat_is_featured = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
#     cat_is_active = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
#     cat_banner = db.Column(db.String(128))
#     cat_icon = db.Column(db.String(128),unique=True, default='')
#     created_at = db.Column(db.DateTime, default=func.now())
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}



# class dg_favorite(db.Model):
#     __tablename__ = 'dg_favorite'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     fav_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
#     u_uid = db.Column(db.String(128), db.ForeignKey('dg_users.u_uid'), nullable=False)
#     room_uid = db.Column(db.String(128), db.ForeignKey('dg_rooms.room_uid'), nullable=True)
#     htl_uid = db.Column(db.String(128), db.ForeignKey('dg_hotels.htl_uid'), nullable=True)
#     status = db.Column(db.Enum(FavoriteStatus), default=FavoriteStatus.ACTIVE.name)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# class dg_tags(db.Model):
#     __tablename__ = 'dg_tags'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     cat_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
#     cat_label = db.Column(db.String(128))
#     cat_is_featured = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
#     cat_is_active = db.Column(db.Boolean(), server_default=expression.true(), nullable=False)
#     status = db.Column(db.Enum(TagStatus), default=TagStatus.ACTIVE.name)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}



# class dg_room(db.Model):
#     __tablename__ = 'dg_room'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     r_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
#     room_name = db.Column(db.String(128), nullable=False)
#     room_type = db.Column(db.String(50), nullable=False)  # ex. "Lecture Room"
#     capacity = db.Column(db.Integer, nullable=False)
#     location = db.Column(db.String(128), nullable=True)  # ex. "First Floor"
#     status = db.Column(db.Enum(RoomStatus), default=RoomStatus.AVAILABLE.name)
#     capacity = db.Column(db.Integer, nullable=False)
#     location = db.Column(db.String(128), nullable=True)  # ex. "First Floor"
#     status = db.Column(db.Enum(RoomStatus), default=RoomStatus.AVAILABLE.name)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


# class dg_room(db.Model):
#     __tablename__ = 'dg_room'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     r_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
#     room_name = db.Column(db.String(128), nullable=False)
#     room_type = db.Column(db.String(50), nullable=False)  # ex. "Lecture Room"
#     capacity = db.Column(db.Integer, nullable=False)
#     location = db.Column(db.String(128), nullable=True)  # ex. "First Floor"
#     status = db.Column(db.Enum(RoomStatus), default=RoomStatus.AVAILABLE.name)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}




# class dg_booking(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     bk_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
#     bk_room_uid = db.Column(db.String(128), db.ForeignKey('dg_rooms.room_uid'))
#     bk_u_uid = db.Column(db.String(128), db.ForeignKey('dg_users.u_uid'))
#     bk_from_date = db.Column(db.String(128))
#     bk_to_date = db.Column(db.String(128))
#     bk_roomcount = db.Column(db.String(128))
#     bk_status = db.Column(db.Enum(BookingStatus), default=BookingStatus.PENDING.name)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     room = db.relationship('dg_room', backref='bookings', lazy=True)  # Relation avec la salle réservée
#     user = db.relationship('dg_users', backref='room_bookings', lazy=True)  # Relation avec l'utilisateur ayant effectué la réservation

#     def as_dict(self):
#        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}



# class dg_contact_us(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     cu_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
#     cu_name = db.Column(db.String(128))
#     cu_email = db.Column(db.String(128))
#     cu_subject = db.Column(db.String(255))
#     cu_body = db.Column(db.Text)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     def as_dict(self):
#        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}



# class dg_orders(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     order_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
#     order_ref = db.Column(db.String(128))
#     order_u_uid = db.Column(db.String(128), db.ForeignKey('dg_users.u_uid'))
#     order_room_uid = db.Column(db.String(128), db.ForeignKey('dg_rooms.room_uid'))
#     order_price = db.Column(db.String(128))
#     total_price = db.Column(db.String(128))
#     mobile_money = db.Column(db.String(128), nullable=False)
#     mobile_network = db.Column(db.String(128), nullable=False)
#     type = db.Column(db.String(128), db.ForeignKey('dg_room_types.room_type_uid'))
#     payment_methode = db.Column(db.String(128))
#     booking_periode = db.Column(db.String(128))
#     status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING.name)
#     creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
#     updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

#     user = db.relationship('dg_users', backref='orders', lazy=True)
#     room = db.relationship('dg_rooms', backref='orders', lazy=True)

#     def as_dict(self):
#         return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
