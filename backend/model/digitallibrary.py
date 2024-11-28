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


class Status(enum.Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    ACTIVE = 'Active'
    BLOCKED = 'Blocked'
    CLOSED = 'Closed'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class UserStatus(enum.Enum):
    ACTIVE = 'Active'
    BLOCKED = 'Blocked'
    SUSPENDED = 'Suspended'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class LoanStatus(enum.Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    RETURNED = 'Returned'
    LOST = 'Lost'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class CollaborationStatus(enum.Enum):
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    CLOSED = 'Closed'
    CANCELLED = 'Cancelled'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class ArticleStatus(enum.Enum):
    DRAFT = 'Draft'
    PUBLISHED = 'Published'
    ARCHIVED = 'Archived'
    REJECTED = 'Rejected'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class ResourceStatus(enum.Enum):
    AVAILABLE = 'Available'
    RESERVED = 'Reserved'
    BORROWED = 'Borrowed'
    ARCHIVED = 'Archived'
    DAMAGED = 'Damaged'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class ReminderStatus(enum.Enum):
    UPCOMING_DUE = 'Upcoming Due'
    OVERDUE = 'Overdue'
    RETURN_CONFIRMED = 'Return Confirmed'
    SENT = 'Sent'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class ReportStatus(enum.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    RESOLVED = 'Resolved'
    CLOSED = 'Closed'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class FavoriteStatus(enum.Enum):
    ACTIVE = 'Active'
    DISABLED = 'Disabled'
    INVALID = 'Invalid'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class TagStatus(enum.Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    PENDING_APPROVAL = 'Pending Approval'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class ReportType(enum.Enum):
    BUG = 'Bug'
    SUGGESTION = 'Suggestion'
    FEATURE = 'Feature'
    LOANS = 'Loans'
    USERS = 'Users'
    BOOKS = 'Books'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class RoomStatus(enum.Enum):
    AVAILABLE = 'Available'
    OCCUPIED = 'Occupied'
    MAINTENANCE = 'Maintenance'
    CLOSED = 'Closed'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class BookingStatus(enum.Enum):
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'
    
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class OrderStatus(Enum):
    PENDING = 'Pending'
    PAID = 'Paid'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'
    REJECTED = 'Rejected'
    REFUNDED = 'Refunded'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
    

class dg_users(db.Model):
    __tablename__ = 'dg_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    u_username = db.Column(db.String(128), unique=True, nullable=False)
    u_name = db.Column(db.String(128))
    u_firstname = db.Column(db.String(128))
    u_lastname = db.Column(db.String(128))
    u_email = db.Column(db.String(100), unique=True, nullable=False)
    u_password_hash = db.Column(db.String(255), nullable=False)
    
    role = db.Column(db.Enum('admin', 'user', 'studient', name='user_roles'), default='user')
    field_of_study = db.Column(db.String(100))
    education_leve = db.Column(db.Enum('professor', 'doctor', 'master' 'licence', 'bts', 'bt' 'bac', name='education_level'), default='bac')
    function = db.Column(db.Enum('professor', 'doctor'))
    u_status = db.Column(db.Enum(UserStatus), default=UserStatus.ACTIVE.name)
    
    created_at = db.Column(db.DateTime, default=func.now())
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    

class dg_user_activity_log(db.Model):
    __tablename__ = 'dg_user_activity_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'))
    activity_type = db.Column(db.String(50))  # login, logout, book_view, etc.
    timestamp = db.Column(db.DateTime, default=func.now())
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    

class dg_user_preferences(db.Model):
    __tablename__ = 'dg_user_preferences'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'))
    preferred_genres = db.Column(db.JSON)
    notification_settings = db.Column(db.JSON)
    language_preference = db.Column(db.String(10))
    theme_preference = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, default=func.now())
    user = db.relationship('dg_users', backref='preferences', lazy=True)

class dg_book(db.Model):
    __tablename__ = 'dg_book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    b_title = db.Column(db.String(255), nullable=False)
    b_author = db.Column(db.String(100), nullable=False)
    b_genre = db.Column(db.String(50))
    b_category = db.Column(db.String(50))
    b_description = db.Column(db.Text)
    b_published_date = db.Column(db.Date)
    b_total_copies = db.Column(db.Integer, default=1)
    b_available_copies = db.Column(db.Integer, default=1)
    

class dg_loan(db.Model):
    __tablename__ = 'dg_loan'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    l_user_u_uid = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'), nullable=False)
    l_book_id = db.Column(db.Integer, db.ForeignKey('dg_book.id'), nullable=False)
    l_date = db.Column(db.DateTime, default=func.now())
    l_return_date = db.Column(db.DateTime)
    l_returned = db.Column(db.Boolean, default=False)
    l_status = db.Column(db.Enum(LoanStatus), default=LoanStatus.PENDING.name)
    

class dg_article(db.Model):
    __tablename__ = 'dg_article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    r_user_u_uid = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'), nullable=False)
    a_title = db.Column(db.String(255), nullable=False)
    a_abstract = db.Column(db.Text, nullable=False)
    a_content = db.Column(db.Text, nullable=False)
    a_publication_date = db.Column(db.DateTime, default=func.now())
    a_publication_status = db.Column(db.Enum('draft', 'published'), default='draft')
    

class dg_reservation(db.Model):
    __tablename__ = 'dg_reservation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rt_user_u_uid = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'), nullable=False)
    rt_book_id = db.Column(db.Integer, db.ForeignKey('dg_book.id'), nullable=False)
    rt_date = db.Column(db.DateTime, default=func.now())
    rt_status = db.Column(db.Enum(Status), default=Status.PENDING.name)
    rt_return_date = db.Column(db.DateTime)
    rt_returned = db.Column(db.Boolean, default=False)
    rt_book_status = db.Column(db.Enum('available', 'reserved', 'borrowed', name ='book_status'), default='available')
    

class dg_review(db.Model):
    __tablename__ = 'dg_review'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rv_user_u_uid = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'), nullable=False)
    rv_book_id = db.Column(db.Integer, db.ForeignKey('dg_book.id'), nullable=False)
    rv_rating = db.Column(db.Integer, nullable=False)
    rv_comment = db.Column(db.Text)
    rv_date = db.Column(db.DateTime, default=func.now())
    created_at = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, default=func.now())
    

class dg_genre(db.Model):
    __tablename__ = 'dg_genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_name = db.Column(db.String(50), unique=True, nullable=False)
    g_description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, default=func.now())
    books = db.relationship('dg_book', backref='dg_genre', lazy=True)
    

class dg_report(db.Model):
    __tablename__ = 'dg_report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rp_title = db.Column(db.String(255), nullable=False)
    rp_description = db.Column(db.Text)
    rp_status = db.Column(db.Enum(ReportStatus), default=ReportStatus.OPEN.name)
    rp_type = db.Column(db.Enum(ReportType), nullable=False)
    rp_date = db.Column(db.DateTime, default=func.now())
    rp_user_u_uid = db.Column(db.Integer, db.ForeignKey('dg_users.u_uid'), nullable=False)
    rp_book_id = db.Column(db.Integer, db.ForeignKey('dg_book.id'), nullable=False)
    rp_user = db.relationship('dg_user', backref='dg_report', lazy=True)
    created_at = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, default=func.now())
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}