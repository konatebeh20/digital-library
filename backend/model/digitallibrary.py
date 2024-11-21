import datetime
import enum
# from sqlalchemy.dialects.postgresql import UUID
import uuid
from cProfile import label
from email.policy import default
from pickle import TRUE

from sqlalchemy.sql import func

from sqlalchemy.sql import expression
from sqlalchemy.sql import text

from config.db import *
from config.db import db

class Status(enum.Enum):
    Y = 'Yes'
    N = 'No'
    
    P = 'Pending'
    C = 'Completed'
    F = 'Failed'
    S = 'Success'
    E = 'Error'
    I = 'In Progress'
    D = 'Done'
    R = 'Rejected'
    A = 'Approved'
    B = 'Blocked'
    O = 'On Hold'
    U = 'Unapproved'
    V = 'Verified'
    X = 'Deleted'
    Z = 'Zipped'
    W = 'Waiting'
    T = 'Timeout'
    M = 'Maintenance'
    L = 'Locked'
    K = 'Killed'
    H = 'Hidden'
    G = 'Ghosted'
    F = 'Frozen'
    E = 'Expired'
    D = 'Draft'
    C = 'Closed'
    B = 'Blocked'
    A = 'Active'
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class go_users(db.Model):
    __tablename__ = 'go_users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    u_name = db.Column(db.String(128))
    u_firstname = db.Column(db.String(128))
    u_lastname = db.Column(db.String(128))
    u_username = db.Column(db.String(128), unique=True)
    u_mobile = db.Column(db.String(128))
    u_address = db.Column(db.String(128))
    u_email = db.Column(db.String(100), unique=True, nullable=False)
    u_city = db.Column(db.String(128))
    u_password_hash = db.Column(db.String(128), nullable=False)
    # u_status = db.Column(db.String(128), default=Status.Y.value)
    # u_status = db.Column(db.Text(), nullable=False, default=0)
    role = db.Column(db.Enum('admin', 'member', name='user_roles'), default='member')
    u_first_login = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    u_id_scan = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=func.now())
    # u_country = db.Column(db.String(128))
    # u_state = db.Column(db.String(128))
    # u_image_link = db.Column(db.Text())
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    

class go_categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    cat_label = db.Column(db.String(128))
    cat_is_featured = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    cat_is_active = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    cat_banner = db.Column(db.String(128))
    cat_icon = db.Column(db.String(128),unique=True, default='')

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class go_tags(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    cat_label = db.Column(db.String(128))
    cat_is_featured = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    cat_is_active = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
class go_rooms(db.Model):
    __tablename__ = 'go_rooms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    hotel_uid = db.Column(db.String(128), db.ForeignKey('go_hotels.htl_uid'), nullable=False)
    room_number = db.Column(db.String(50), nullable=False)
    room_type_uid = db.Column(db.String(128), db.ForeignKey('go_room_types.room_type_uid'), nullable=False)  
    room_capacity = db.Column(db.Integer, nullable=False)
    room_display_times = db.Column(db.Float, nullable=False)
    room_price = db.Column(db.Float, nullable=False)
    room_beds_number = db.Column(db.String(100), nullable=False)
    room_amenities = db.Column(db.JSON)  
    room_description = db.Column(db.Text, nullable=True)
    room_images = db.Column(db.JSON)  
    room_position = db.Column(db.Integer)
    room_status = db.Column(db.String(20), nullable=False, default='available')
    favorite = db.Column(db.Text, default=False, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
   
   
class go_favorite(db.Model):
    __tablename__ = 'go_favorite'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fav_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    u_uid = db.Column(db.String(128), db.ForeignKey('go_users.u_uid'), nullable=False)
    room_uid = db.Column(db.String(128), db.ForeignKey('go_rooms.room_uid'), nullable=True)
    htl_uid = db.Column(db.String(128), db.ForeignKey('go_hotels.htl_uid'), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
   
class go_room_types(db.Model):
    __tablename__ = 'go_room_types'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_type_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255))
    max_capacity = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.JSON, nullable=False) 
    status = db.Column(db.String(20), nullable=False) 
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
    
class go_room_taxes(db.Model):
    __tablename__ = 'go_room_taxes'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tax_uid = db.Column(db.String(128), unique=True, default=lambda: str(uuid.uuid4()))
    room_type_uid = db.Column(db.String(128), db.ForeignKey('go_room_types.room_type_uid'))
    tax_name = db.Column(db.String(128), nullable=False)
    tax_rate = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False) 
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)


    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class go_booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bk_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))

    bk_roomid = db.Column(db.String(128), db.ForeignKey('go_rooms.room_uid'))
    bk_userid = db.Column(db.String(128), db.ForeignKey('go_users.u_uid'))
    bk_from_date = db.Column(db.String(128))
    bk_to_date = db.Column(db.String(128))
    bk_roomcount = db.Column(db.String(128))
    bk_status = db.Column(db.String(128))

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class go_hotels(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    htl_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))

    htl_title = db.Column(db.String(128))
    htl_status = db.Column(db.Boolean(),server_default=expression.true(), nullable=False)
    htl_stars = db.Column(db.Integer)
    htl_address = db.Column(db.String(128))
    htl_description = db.Column(db.Text)
    htl_amenities = db.Column(db.JSON)  
    htl_longitude = db.Column(db.String(128))
    htl_latitude = db.Column(db.String(128))
    htl_tel_number = db.Column(db.String(128))
    htl_feature_image = db.Column(db.String(128))
    htl_room_quantity = db.Column(db.String(128))
    htl_category = db.Column(db.String(128), db.ForeignKey('go_categories.cat_uid'))


    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class go_contact_us(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ct_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))

    ct_name = db.Column(db.String(128))
    ct_email = db.Column(db.String(128))
    ct_subject = db.Column(db.String(255))
    ct_body = db.Column(db.Text)

    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class go_orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_uid = db.Column(db.String(128),unique=True, default=lambda: str(uuid.uuid4()))
    order_ref = db.Column(db.String(128))
    u_uid = db.Column(db.String(128), db.ForeignKey('go_users.u_uid'))
    room_uid = db.Column(db.String(128), db.ForeignKey('go_rooms.room_uid'))
    occupants_adults = db.Column(db.Integer, nullable=False)
    occupants_children = db.Column(db.Integer, nullable=False)
    coupon = db.Column(db.String(128))
    price = db.Column(db.String(128))
    total_price = db.Column(db.String(128))
    taxe = db.Column(db.String(128), nullable=False)
    mobile_money = db.Column(db.String(128), nullable=False)
    mobile_network = db.Column(db.String(128), nullable=False)
    type = db.Column(db.String(128), db.ForeignKey('go_room_types.room_type_uid'))
    payment_methode = db.Column(db.String(128))
    booking_periode = db.Column(db.String(128))
    status = db.Column(db.String(128))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    
    def as_dict(self):
       return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
   