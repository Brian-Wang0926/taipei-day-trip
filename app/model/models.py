from .. import db
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import Date

# 定義資料模型
class Attraction(db.Model):
    __tablename__ = 'attractions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    transport = db.Column(db.Text)
    mrt = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, name, category, description, address, transport, mrt, lat, lng):
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.transport = transport
        self.mrt = mrt
        self.lat = lat
        self.lng = lng

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'))
    img = db.Column(db.String(255))

    def __init__(self, attraction_id, img):
        self.attraction_id = attraction_id
        self.img = img

# 設定外鍵關係
Attraction.images = db.relationship('Image', backref='attraction', lazy=True)

# 建立會員資料庫
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password).decode('utf-8')
        
# 建立預定景點資料庫
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(Date)
    time = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def __init__(self, attraction_id, user_id, date, time, price):
        self.attraction_id = attraction_id
        self.user_id = user_id
        self.date = date
        self.time = time
        self.price = price

    attraction = db.relationship('Attraction',backref='bookings')
    user = db.relationship('User',backref='users')

# 建立訂單資料庫